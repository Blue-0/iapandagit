import pandas as pd
import sqlite3
import chainlit as cl
import subprocess
from pandasai import SmartDataframe
from langchain_community.llms import Ollama
import os

# 📌 Fonction pour récupérer les modèles installés dans Ollama
def get_available_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            models = [line.split()[0] for line in result.stdout.strip().split("\n")[1:]]
            return models
    except Exception:
        return ["llama3", "mistral", "deepseek"]
    return []

@cl.on_chat_start
async def start_chat():
    # Set initial message history
    cl.user_session.set("message_history", [{"role": "system", "content": "You are a helpful assistant."}])

    # Sélection du modèle IA (correction ici)
    available_models = get_available_models()
    selected_model = await cl.Select(
        content="🧠 Sélectionnez un modèle IA disponible :",
        choices=available_models
    ).send()

    # Stocker le modèle sélectionné dans la session utilisateur
    cl.user_session.set("selected_model", selected_model['content'])

    # Demander à l'utilisateur d'uploader un fichier Excel
    uploaded_file = await cl.AskFileMessage(
        content="📂 Téléchargez un fichier Excel à analyser (.xlsx) :",
        accept=[".xlsx"]
    ).send()

    if uploaded_file:
        # Lire le fichier Excel
        df = pd.read_excel(uploaded_file["path"], engine='openpyxl')
        cl.user_session.set("dataframe", df)

        await cl.Message(content="✅ Fichier Excel chargé avec succès ! Posez votre question.").send()

@cl.on_message
async def main(message: cl.Message):
    # Récupérer l'historique des messages
    message_history = cl.user_session.get("message_history")
    message_history.append({"role": "user", "content": message.content})

    # Récupérer le DataFrame et le modèle sélectionné
    df = cl.user_session.get("dataframe")
    selected_model = cl.user_session.get("selected_model")

    if df is None:
        await cl.Message(content="⚠️ Aucun fichier Excel chargé. Veuillez en uploader un.").send()
        return

    # Initialiser l'IA avec le modèle sélectionné
    llm = Ollama(model=selected_model)

    # Convertir le DataFrame en SmartDataframe pour PandasAI
    df = SmartDataframe(df, config={"llm": llm})

    # Poser la question à l'IA
    question = message.content
    response = df.chat(question)

    msg = cl.Message(content=response)
    await msg.send()

    # Mettre à jour l'historique et envoyer la réponse finale
    message_history.append({"role": "assistant", "content": msg.content})
    await msg.update()
