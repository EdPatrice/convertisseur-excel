import streamlit as st
import pandas as pd
from conversion import encoding
import io

st.title("Convertisseur de Fichier Excel")
st.markdown("<br><br>", unsafe_allow_html=True)
# Ajout de la description et exemple
st.markdown("""
Cette application vous aide à convertir les valeurs numériques de votre fichier Excel dans un format encodé spécifique. 
L'application traite la première colonne de votre fichier Excel, en ne gardant que les valeurs numériques et en les convertissant selon nos règles d'encodage. 
Par exemple, si votre fichier Excel contient une valeur comme '12345' dans la première colonne, elle sera convertie en son équivalent encodé. 
Les valeurs non numériques seront automatiquement filtrées pour assurer une conversion précise.
""")
st.markdown("<br><br>", unsafe_allow_html=True)

# Séparation visuelle
st.markdown("---")

st.write("Téléchargez un fichier Excel pour convertir les valeurs de la première colonne.")

# Téléchargement de fichier
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx"])

if uploaded_file is not None:
    # Lecture du fichier Excel
    df = pd.read_excel(uploaded_file, header=None)
    
    # Traitement des données
    df[0] = df[0].astype(str).str.strip()
    df['is_numeric'] = df[0].str.isnumeric()
    
    # Comptage et affichage des lignes non numériques
    non_numeric_count = (~df['is_numeric']).sum()
    if non_numeric_count > 0:
        st.warning(f"Trouvé {non_numeric_count} ligne(s) contenant des valeurs non numériques. Elles seront supprimées.")
    
    # Filtrage des lignes numériques
    df = df[df['is_numeric']].drop('is_numeric', axis=1)
    
    # Conversion des valeurs
    df[1] = df[0].apply(encoding)
    
    # Renommage des colonnes
    df.columns = ['Original', 'Converti']
    
    # Affichage du tableau converti
    st.write("Données Converties:")
    st.dataframe(df)
    
    # Création d'un buffer pour sauvegarder le fichier Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # Bouton de téléchargement
    st.download_button(
        label="Télécharger le fichier Excel converti",
        data=buffer.getvalue(),
        file_name="donnees_converties.xlsx",
        mime="application/vnd.ms-excel"
    )