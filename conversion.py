def conversion(nomFichierOriginal, nomFichierConversion):
    import pandas as pd

    # Lire le fichier CSV d'origine
    df = pd.read_excel(nomFichierOriginal, header=None)
    
    # Vérifier si la première colonne contient uniquement des nombres
    # Convertir en string d'abord pour gérer les nombres et supprimer les espaces
    df[0] = df[0].astype(str).str.strip()
    
    # Garder seulement les lignes qui contiennent des nombres
    df['is_numeric'] = df[0].str.isnumeric()
    
    # Compter les lignes non numériques avant de les supprimer
    non_numeric_count = (~df['is_numeric']).sum()
    if non_numeric_count > 0:
        print(f"Suppression de {non_numeric_count} ligne(s) contenant des valeurs non numériques.")
    
    # Filtrer pour ne garder que les lignes avec des valeurs numériques
    df = df[df['is_numeric']].drop('is_numeric', axis=1)
    
    # Convertir les valeurs de la première colonne
    df[1] = df[0].apply(encoding)
    
    # Enregistrer les valeurs converties dans le nouveau fichier CSV
    df.to_excel(nomFichierConversion, index=False, header=['Original', 'Converti'])

    print(f"Les valeurs converties sont enregistrées dans le fichier: '{nomFichierConversion}'")
    return df


# Fonction d'encodage
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
    
    return ''.join(sorted(converted))