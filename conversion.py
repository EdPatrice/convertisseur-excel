def encoding(test_value):
    code = "0-5 1-4 2-7 3-8 6-9".split()
    a = [x.split('-')[0] for x in code]
    b = [x.split('-')[1] for x in code]
    
    converted = ''
    value_is_number = isinstance(test_value, (int, float))
    if (value_is_number):
        for char in str(test_value):
            if char in a:
                converted += char
            elif char in b:
                converted += a[b.index(char)]
        
        return converted, ''.join(sorted(converted))
    else: 
        return None, None

def conversion(nomFichierOriginal, nomFichierConversion):
    import pandas as pd
    import numpy as np

    # Lire le fichier Excel d'origine
    df = pd.read_excel(nomFichierOriginal, header=None)
    
    # Créer un writer Excel pour sauvegarder plusieurs feuilles
    with pd.ExcelWriter(nomFichierConversion) as writer:
        # Sauvegarder les données originales
        df.to_excel(writer, sheet_name='Original', index=False)
        
        # Créer des DataFrames pour les valeurs converties
        df_unsorted = pd.DataFrame(index=range(len(df)))
        df_sorted = pd.DataFrame(index=range(len(df)))
        
        # Parcourir toutes les colonnes qui contiennent des données
        for col in df.columns:
            # Convertir en string et supprimer les espaces
            df[col] = df[col].astype(str).str.strip()
            col_name = f"Col_{col+1}"
            
            # Initialiser les colonnes avec les valeurs originales
            df_unsorted[col_name] = df[col]
            df_sorted[col_name] = df[col]
            
            # Traiter chaque valeur dans la colonne
            for idx, value in df[col].items():
                # if value.isnumeric():  # Traiter seulement les valeurs numériques
                unsorted, sorted_val = encoding(value)
                df_unsorted.at[idx, col_name] = unsorted
                df_sorted.at[idx, col_name] = sorted_val
        
        # Sauvegarder les feuilles converties
        if not df_unsorted.empty:
            df_unsorted.to_excel(writer, sheet_name='Converti_Non_Trie', index=False)
            df_sorted.to_excel(writer, sheet_name='Converti_Trie', index=False)
        
    print(f"Les valeurs converties sont enregistrées dans le fichier: '{nomFichierConversion}'")
    return df_unsorted, df_sorted