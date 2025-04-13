def encoding(test_value):
    code = "0-5 1-4 2-7 3-8 6-9".split()
    a = [x.split('-')[0] for x in code]
    b = [x.split('-')[1] for x in code]
    
    converted = ''
    for char in str(test_value):
        if char in a:
            converted += char
        elif char in b:
            converted += a[b.index(char)]
    
    return converted, ''.join(sorted(converted))

def conversion(nomFichierOriginal, nomFichierConversion):
    import pandas as pd

    # Lire le fichier Excel d'origine
    df = pd.read_excel(nomFichierOriginal, header=None)
    
    # Créer un writer Excel pour sauvegarder plusieurs feuilles
    with pd.ExcelWriter(nomFichierConversion) as writer:
        # Sauvegarder les données originales
        df.to_excel(writer, sheet_name='Original', index=False)
        
        # Créer des DataFrames pour les valeurs converties
        df_unsorted = pd.DataFrame()
        df_sorted = pd.DataFrame()
        
        # Parcourir toutes les colonnes qui contiennent des données
        for col in df.columns:
            # Convertir en string et supprimer les espaces
            df[col] = df[col].astype(str).str.strip()
            
            # Vérifier si les valeurs sont numériques
            numeric_mask = df[col].str.isnumeric()
            
            if numeric_mask.any():
                # Appliquer la conversion et récupérer les deux versions
                conversions = df[col][numeric_mask].apply(encoding)
                unsorted_values = [x[0] for x in conversions]
                sorted_values = [x[1] for x in conversions]
                
                # Ajouter les colonnes aux DataFrames
                col_name = f"Col_{col+1}"
                df_unsorted[col_name] = pd.Series(unsorted_values)
                df_sorted[col_name] = pd.Series(sorted_values)
        
        # Sauvegarder les feuilles converties
        if not df_unsorted.empty:
            df_unsorted.to_excel(writer, sheet_name='Converti_Non_Trie', index=False)
            df_sorted.to_excel(writer, sheet_name='Converti_Trie', index=False)
        
    print(f"Les valeurs converties sont enregistrées dans le fichier: '{nomFichierConversion}'")
    return df_unsorted, df_sorted