import streamlit as st
import pandas as pd
from conversion import encoding
import io

st.title("Convertisseur de Fichier Excel")
st.markdown("<br><br>", unsafe_allow_html=True)
# Ajout de la description et exemple
st.markdown("""
Cette application vous aide à convertir les valeurs numériques de votre fichier Excel dans un format encodé spécifique. 
L'application traite toutes les colonnes de votre fichier Excel, en ne gardant que les valeurs numériques et en les convertissant selon nos règles d'encodage.
Pour chaque valeur convertie, vous obtiendrez deux versions :
- La version convertie non triée
- La version convertie triée en ordre croissant
""")
st.markdown("<br><br>", unsafe_allow_html=True)

# Séparation visuelle
st.markdown("---")

st.write("Téléchargez un fichier Excel pour convertir les valeurs.")

# Téléchargement de fichier
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx"])

if uploaded_file is not None:
    # Lecture du fichier Excel
    df_original = pd.read_excel(uploaded_file, header=None)
    
    # Initialisation des DataFrames pour les versions converties
    df_unsorted = pd.DataFrame()
    df_sorted = pd.DataFrame()
    
    # Traitement de chaque colonne
    for col in df_original.columns:
        # Conversion en string et nettoyage
        df_original[col] = df_original[col].astype(str).str.strip()
        numeric_mask = df_original[col].str.isnumeric()
        
        if numeric_mask.any():
            # Conversion des valeurs numériques
            conversions = df_original[col][numeric_mask].apply(encoding)
            unsorted_values = [x[0] for x in conversions]
            sorted_values = [x[1] for x in conversions]
            
            # Ajout des colonnes converties
            col_name = f"Col_{col+1}"
            df_unsorted[col_name] = pd.Series(unsorted_values)
            df_sorted[col_name] = pd.Series(sorted_values)
    
    # Affichage des données
    st.write("Données originales:")
    st.dataframe(df_original)
    
    if not df_unsorted.empty:
        st.write("Données converties (non triées):")
        st.dataframe(df_unsorted)
        
        st.write("Données converties (triées):")
        st.dataframe(df_sorted)
        
        # Création d'un buffer pour sauvegarder le fichier Excel avec les trois feuilles
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_original.to_excel(writer, sheet_name='Original', index=False)
            df_unsorted.to_excel(writer, sheet_name='Converti_Non_Trie', index=False)
            df_sorted.to_excel(writer, sheet_name='Converti_Trie', index=False)
        
        # Bouton de téléchargement
        st.download_button(
            label="Télécharger le fichier Excel avec les valeurs converties.",
            data=buffer.getvalue(),
            file_name="donnees_converties.xlsx",
            mime="application/vnd.ms-excel"
        )
    else:
        st.warning("Aucune valeur numérique n'a été trouvée dans le fichier.")