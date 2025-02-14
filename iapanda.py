import pandas as pd
import sqlite3
import chainlit as cl
import subprocess
from pandasai import SmartDataframe
from langchain_community.llms import Ollama
from sqlalchemy import create_engine

# 📌 Fonction pour récupérer les modèles disponibles dans Ollama
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
    # Étape 1 : Sélection du modèle IA
    available_models = get_available_models()
    model_select = cl.Select(
        id="model_select",
        label="🧠 Sélectionnez un modèle IA",
        values=available_models,
        initial_index=0,
    )
    await model_select.send()

    # Attendre la sélection du modèle
    settings = await cl.ChatSettings([model_select]).send()
    selected_model = settings["model_select"]

    cl.user_session.set("selected_model", selected_model)

    # Étape 2 : Téléversement du fichier Excel
    uploaded_file = await cl.AskFileMessage(
        content="📂 **Téléversez un fichier Excel à analyser :**",
        accept=[".xlsx"]
    ).send()

    if uploaded_file:
        # Lire le fichier Excel
        df = pd.read_excel(uploaded_file["path"], engine='openpyxl')

        # Stocker les données en session
        cl.user_session.set("dataframe", df)

        # Étape 3 : Créer la base de données SQLite
        engine = create_engine('sqlite:///database.db')
        df.to_sql("data_table", engine, if_exists="replace", index=False)

        # Afficher un aperçu des données dans l'interface
        preview_message = f"📊 **Aperçu des données (5 premières lignes) :**\n\n{df.head().to_markdown()}"
        await cl.Message(content=preview_message).send()

        await cl.Message(content="✅ **Base de données créée avec succès ! Posez vos questions.**").send()

@cl.on_message
async def main(message: cl.Message):
    # Récupérer le DataFrame et le modèle sélectionné
    df = cl.user_session.get("dataframe")
    selected_model = cl.user_session.get("selected_model")

    if df is None:
        await cl.Message(content="⚠️ Aucun fichier chargé. Veuillez téléverser un fichier Excel.").send()
        return

    # Initialiser l'IA avec le modèle sélectionné
    llm = Ollama(model=selected_model)

    # Convertir le DataFrame en SmartDataframe pour PandasAI
    sdf = SmartDataframe(df, config={"llm": llm})

    # Poser la question à l'IA
    question = message.content
    response = sdf.chat(question)

    await cl.Message(content=response).send()
