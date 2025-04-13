import streamlit as st
import pandas as pd
import numpy as np
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

Note: L'application convertira toutes les valeurs numériques dans chaque colonne, même si certaines colonnes contiennent des valeurs non numériques.
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
    
    # Créer des DataFrames pour les valeurs converties avec le même nombre de lignes que l'original
    df_unsorted = pd.DataFrame(index=range(len(df_original)))
    df_sorted = pd.DataFrame(index=range(len(df_original)))
    
    # Traitement de chaque colonne
    for col in df_original.columns:
        # Conversion en string et nettoyage
        # df_original[col] = df_original[col].astype(str).str.strip()
        # df_original[col] = df_original[col].astype(int)
        col_name = f"Col_{col+1}"
        
        # Initialiser les colonnes avec NaN
        # df_unsorted[col_name] = np.nan
        # df_sorted[col_name] = np.nan
        
        # Traiter chaque valeur individuellement
        for idx, value in df_original[col].items():
            # if value.isnumeric():  # Traiter seulement les valeurs numériques
            unsorted, sorted_val = encoding(value)
            df_unsorted.at[idx, col_name] = unsorted
            df_sorted.at[idx, col_name] = sorted_val
    
    # Affichage des données
    st.write("Données originales:")
    st.dataframe(df_original)
    
    if not df_unsorted.empty: #and df_unsorted.notna().any().any():
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
            label="Télécharger le fichier Excel avec les trois feuilles",
            data=buffer.getvalue(),
            file_name="donnees_converties.xlsx",
            mime="application/vnd.ms-excel"
        )
    else:
        st.warning("Aucune valeur numérique n'a été trouvée dans le fichier.")