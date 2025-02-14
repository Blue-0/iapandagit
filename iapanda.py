import streamlit as st
import pandas as pd
import ollama

def excel_to_markdown(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df.to_markdown(index=False)

# Interface Streamlit
st.title("📊 Analyse de fichiers Excel avec LLaMA")

uploaded_file = st.file_uploader("📂 Téléchargez un fichier Excel", type=["xlsx"])

if uploaded_file:
    markdown_data = excel_to_markdown(uploaded_file)
    
    # Affichage du tableau Markdown
    st.write("📜 **Données converties en Markdown :**")
    st.code(markdown_data, language="markdown")

    # Question de l'utilisateur
    question = st.text_input("💬 Posez une question sur ces données")

    if st.button("🔎 Analyser avec LLaMA"):
        if question:
            prompt = f"Voici un tableau de données :\n\n{markdown_data}\n\nQuestion : {question}"
            
            response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
            ai_response = response["message"]["content"]

            st.write("🧠 **Réponse de LLaMA :**")
            st.write(ai_response)
