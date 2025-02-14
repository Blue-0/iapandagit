import streamlit as st
import pandas as pd
import ollama
import tabulate

# 📌 Fonction pour convertir un fichier Excel en Markdown
def excel_to_markdown(file):
    df = pd.read_excel(file, engine='openpyxl')  # Charger le fichier Excel
    return df.to_markdown(index=False)  # Convertir en Markdown

# 🎯 Interface Streamlit
st.set_page_config(page_title="Analyse Excel avec LLaMA", layout="wide")

st.title("📊 Analyse de Fichiers Excel avec LLaMA")

# 📂 Télécharger un fichier Excel
uploaded_file = st.file_uploader("📂 Téléchargez un fichier Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    # 📌 Convertir en Markdown
    markdown_data = excel_to_markdown(uploaded_file)

    # 🔍 Afficher un aperçu des données en Markdown
    st.subheader("📜 **Données converties en Markdown :**")
    st.code(markdown_data, language="markdown")

    # 💬 Demander une question à l'utilisateur
    question = st.text_area("💬 Posez une question à l'IA sur ces données", height=100)

    # 🏆 Analyser avec LLaMA
    if st.button("🔎 Analyser avec LLaMA") and question:
        with st.spinner("🔄 L'IA réfléchit..."):

            # 📝 Construire le prompt
            prompt = f"""
            Tu es un expert en analyse de données.
            Voici un tableau extrait d’un fichier Excel contenant des informations :

            {markdown_data}

            ❓ Question : {question}
            Réponds en te basant uniquement sur ces données.
            """

            # 💡 Exécuter LLaMA
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            ai_response = response["message"]["content"]

        # 🔥 Afficher la réponse de LLaMA
        st.subheader("🧠 **Réponse de LLaMA :**")
        st.write(ai_response)

    # 🎯 Bouton pour réinitialiser la conversation
    if st.button("🔄 Réinitialiser"):
        st.experimental_rerun()
