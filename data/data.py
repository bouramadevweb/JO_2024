import pandas as pd
import json

# Lire le fichier JSON en utilisant l'encodage UTF-8
with open('C:/Users/maitr/OneDrive/Bureau/JO_2024_Django/JeuxOlympique/data/data_2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Transformer les données en DataFrame Pandas
df = pd.DataFrame(data)

# Enregistrer le DataFrame en CSV en utilisant l'encodage UTF-8
df.to_csv('C:/Users/maitr/OneDrive/Bureau/JO_2024_Django/JeuxOlympique/data/data.csv', index=False, encoding='utf-8')
