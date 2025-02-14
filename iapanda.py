import streamlit as st
import pandas as pd
import ollama
import subprocess

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

# 📌 Fonction pour convertir un fichier Excel en Markdown
def excel_to_markdown(file):
    df = pd.read_excel(file, engine='openpyxl')  # Charger le fichier Excel
    return df.to_markdown(index=False)  # Convertir en Markdown

# 🎯 Interface Streamlit
st.set_page_config(page_title="Analyse Excel avec LLaMA", layout="wide")

st.title("📊 Analyse de Fichiers Excel avec Ollama")

# 📂 Télécharger un fichier Excel
uploaded_file = st.file_uploader("📂 Téléchargez un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # 📌 Convertir en Markdown
    markdown_data = excel_to_markdown(uploaded_file)

    # 🔍 Afficher un aperçu des données en Markdown
    st.subheader("📜 **Données converties en Markdown :**")
    st.code(markdown_data, language="markdown")

    # 🎯 Sélection du modèle IA disponible sur Ollama
    available_models = get_available_models()
    selected_model = st.selectbox("🧠 **Sélectionnez un modèle IA disponible** :", available_models)

    # 💬 Demander une question à l'utilisateur
    question = st.text_area("💬 Posez une question à l'IA sur ces données", height=100)

    # 🏆 Analyser avec LLaMA
    if st.button("🔎 Analyser avec l’IA") and question:
        with st.spinner("🔄 L'IA réfléchit..."):

            # 📝 Construire le prompt
            prompt = f"""
            Tu es un expert en analyse de données.
            Voici un tableau extrait d’un fichier Excel contenant des informations :

            {markdown_data}

            ❓ Question : {question}
            Réponds en te basant uniquement sur ces données.
            """

            # 💡 Exécuter le modèle IA sélectionné
            response = ollama.chat(model=selected_model, messages=[{"role": "user", "content": prompt}])
            ai_response = response["message"]["content"]

        # 🔥 Afficher la réponse de l'IA
        st.subheader("🧠 **Réponse de l'IA :**")
        st.write(ai_response)

    # 🎯 Bouton pour réinitialiser la conversation
    if st.button("🔄 Réinitialiser"):
        st.experimental_rerun()
