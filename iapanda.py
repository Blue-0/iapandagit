import streamlit as st
import pandas as pd

# Titre de l'application
st.title("Analyse de Fichiers Excel Volumineux")

# Téléchargement du fichier Excel
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx"])

if uploaded_file is not None:
    # Lecture du fichier Excel
    df = pd.read_excel(uploaded_file, engine='openpyxl')
    
    # Affichage des dimensions du DataFrame
    st.write(f"Le fichier contient {df.shape[0]} lignes et {df.shape[1]} colonnes.")
    
    # Affichage des premières lignes du DataFrame
    st.write("Aperçu des données :")
    st.dataframe(df.head())
    
    # Affichage de statistiques descriptives
    st.write("Statistiques descriptives :")
    st.write(df.describe())
    
    # Sélection de colonnes pour l'analyse
    selected_columns = st.multiselect("Sélectionnez les colonnes à analyser", df.columns)
    
    if selected_columns:
        st.write("Données sélectionnées :")
        st.dataframe(df[selected_columns].head())
        
        # Affichage de corrélations
        st.write("Matrice de corrélation :")
        st.write(df[selected_columns].corr())
    else:
        st.write("Veuillez sélectionner au moins une colonne pour l'analyse.")
