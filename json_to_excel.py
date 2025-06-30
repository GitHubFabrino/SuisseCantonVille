import json
import pandas as pd
from pathlib import Path

def json_to_excel(json_file_path, excel_file_path=None):
    # Si aucun chemin de sortie n'est spécifié, on utilise le même nom que le fichier JSON avec l'extension .xlsx
    if excel_file_path is None:
        excel_file_path = Path(json_file_path).with_suffix('.xlsx')
    
    # Lire le fichier JSON
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Créer une liste pour stocker les données des cantons
    rows = []
    
    # Parcourir chaque canton
    for canton in data:
        canton_name = canton.get('nom_canton', '')
        code_canton = canton.get('code', '')
        
        # Récupérer toutes les villes du canton et les nettoyer
        villes = [ville.get('nom_ville', '').strip() for ville in canton.get('villeListe', [])]
        # Trier les villes par ordre alphabétique
        villes_triees = sorted(villes)
        # Joindre les villes avec des virgules et des espaces
        villes_texte = ', '.join(villes_triees)
        
        # Ajouter une ligne pour ce canton
        rows.append({
            'Canton': canton_name,
            'Code Canton': code_canton,
            'Villes': villes_texte,
            'Nombre de villes': len(villes_triees)
        })
    
    # Créer un DataFrame avec les données
    df = pd.DataFrame(rows)
    
    # Trier les données par nom de canton
    df = df.sort_values(by='Canton')
    
    # Créer un writer pour formater les colonnes
    with pd.ExcelWriter(excel_file_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Cantons et Villes')
        
        # Ajuster la largeur des colonnes
        worksheet = writer.sheets['Cantons et Villes']
        worksheet.column_dimensions['A'].width = 20  # Canton
        worksheet.column_dimensions['B'].width = 15  # Code Canton
        worksheet.column_dimensions['C'].width = 80  # Villes
        worksheet.column_dimensions['D'].width = 15  # Nombre de villes
    
    return str(excel_file_path)

if __name__ == "__main__":
    # Chemin du fichier JSON d'entrée
    json_file = r"c:\Users\MADA-Digital\dev\Scrapy\dataSuisse\ville\monprojet\cantons_et_villes_geolocalises.json"
    
    try:
        # Convertir le JSON en Excel
        output_file = json_to_excel(json_file)
        print(f"Le fichier Excel a été créé avec succès : {output_file}")
    except Exception as e:
        print(f"Une erreur s'est produite : {str(e)}")
