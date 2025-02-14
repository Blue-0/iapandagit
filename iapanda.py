import pandas as pd
import chainlit as cl
import subprocess
from pandasai import SmartDataframe
from langchain_community.llms import Ollama

# Fonction pour récupérer les modèles disponibles dans Ollama
def get_available_models():
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if result.returncode == 0:
            models = [line.split()[0] for line in result.stdout.strip().split("\n")[1:]]
            return models
    except Exception:
        return ["llama3", "mistral", "deepseek"]
    return []

# Fonction appelée au démarrage du chat
@cl.on_chat_start
async def start_chat():
    # Récupérer les modèles disponibles
    available_models = get_available_models()

    # Demander à l'utilisateur de sélectionner un modèle
    settings = await cl.ChatSettings(
        [
            cl.Select(
                id="model_select",
                label="Sélectionnez un modèle IA",
                values=available_models,
                initial_index=0,
            )
        ]
    ).send()

    # Récupérer le modèle sélectionné
    selected_model = settings["model_select"]

    # Stocker le modèle sélectionné dans la session utilisateur
    cl.user_session.set("selected_model", selected_model)

    # Demander à l'utilisateur de télécharger un fichier Excel
    uploaded_file = await cl.AskFileMessage(
        content="Veuillez télécharger le fichier Excel à analyser.",
        accept=[".xlsx"]
    ).send()

    if uploaded_file:
        # Lire le fichier Excel
        df = pd.read_excel(uploaded_file["path"], engine='openpyxl')
        cl.user_session.set("dataframe", df)

        await cl.Message(content="Fichier Excel chargé avec succès ! Vous pouvez maintenant poser vos questions.").send()

# Fonction appelée lorsqu'un message est reçu
@cl.on_message
async def main(message: cl.Message):
    # Récupérer le DataFrame et le modèle sélectionné
    df = cl.user_session.get("dataframe")
    selected_model = cl.user_session.get("selected_model")

    if df is None:
        await cl.Message(content="Aucun fichier Excel n'a été chargé. Veuillez télécharger un fichier pour continuer.").send()
        return

    # Initialiser l'IA avec le modèle sélectionné
    llm = Ollama(model=selected_model)

    # Convertir le DataFrame en SmartDataframe pour PandasAI
    sdf = SmartDataframe(df, config={"llm": llm})

    # Poser la question à l'IA
    question = message.content
    response = sdf.chat(question)

    await cl.Message(content=response).send()
