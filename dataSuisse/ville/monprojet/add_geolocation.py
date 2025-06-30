import json
import time
import re
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Configuration de l'utilisateur pour Nominatim
geolocator = Nominatim(user_agent="swiss_cantons_cities_geocoder", timeout=10)
# Ajout d'un délai entre les requêtes (1.5 secondes pour respecter les limites de l'API)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.5, error_wait_seconds=10, max_retries=2)

# Mappage des noms de cantons pour la recherche
def get_location(query, canton_code=None):
    """
    Récupère les coordonnées géographiques pour une requête donnée
    """
    # Nettoyer la requête
    query = query.strip()
    
    # Essayer différentes variantes de la requête
    queries_to_try = [f"{query}, Switzerland"]
    
    # Si on a un code de canton, essayer avec
    if canton_code:
        queries_to_try.append(f"{query}, {canton_code}, Switzerland")
    
    # Essayer sans les parties entre parenthèses si présentes
    if '(' in query:
        base_query = re.sub(r'\s*\([^)]*\)', '', query).strip()
        queries_to_try.append(f"{base_query}, Switzerland")
        if canton_code:
            queries_to_try.append(f"{base_query}, {canton_code}, Switzerland")
    
    # Essayer chaque variante jusqu'à ce qu'on trouve un résultat
    for q in queries_to_try:
        try:
            location = geocode(q, exactly_one=True, addressdetails=True, language='fr')
            if location:
                # Vérifier que c'est bien en Suisse
                if location.raw.get('address', {}).get('country_code', '').lower() == 'ch':
                    return {
                        "lat": location.latitude,
                        "lon": location.longitude,
                        "display_name": location.address
                    }
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"  Erreur pour '{q}': {str(e)}")
            time.sleep(2)  # Attendre un peu plus longtemps en cas d'erreur
    
    print(f"  Impossible de géolocaliser: {query}")
    return None

def add_geolocation(input_file, output_file):
    # Charger les données existantes
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Pour chaque canton
    for canton in data:
        canton_name = canton['nom_canton']
        canton_code = canton.get('code', '')
        print(f"Traitement du canton: {canton_name} ({canton_code})")
        
        # Mappage des noms de cantons pour la recherche
        canton_mapping = {
            "Appenzell Rh.-E": "Appenzell Ausserrhoden",
            "Appenzell Rh.-I": "Appenzell Innerrhoden",
            "Bâle-Campagne": "Basel-Landschaft",
            "Bâle-Ville": "Basel-Stadt",
            "Fribourg": "Fribourg",
            "Genève": "Genève",
            "Glaris": "Glarus",
            "Grisons": "Graubünden",
            "Neuchâtel": "Neuchâtel",
            "St-Gall": "Sankt Gallen",
            "Schaffhouse": "Schaffhausen",
            "Schwytz": "Schwyz",
            "Tessin": "Ticino",
            "Thurgovie": "Thurgau",
            "Valais": "Valais",
            "Vaud": "Vaud",
            "Zoug": "Zug",
            "Zurich": "Zürich"
        }
        
        # Utiliser le nom mappé si disponible, sinon utiliser le nom original
        search_canton_name = canton_mapping.get(canton_name, canton_name)
        
        # Ajouter la géolocalisation du canton
        if 'geoLocation' not in canton:
            # Essayer d'abord avec le nom mappé
            canton_location = get_location(search_canton_name, canton_code)
            
            # Si pas trouvé, essayer avec le nom original
            if not canton_location and search_canton_name != canton_name:
                canton_location = get_location(canton_name, canton_code)
            
            # Si on a une localisation, l'ajouter
            if canton_location:
                canton['geoLocation'] = canton_location
                print(f"  Canton géolocalisé: {canton_location.get('display_name', '')}")
        
        # Ne pas géolocaliser les villes, seulement les cantons
        # Les villes conserveront leur structure actuelle sans coordonnées
    
    # Sauvegarder les données mises à jour
    
    # Sauvegarder les données mises à jour
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\nGéolocalisation des cantons terminée. Données sauvegardées dans {output_file}")
    print("Remarque: Seuls les cantons ont été géolocalisés, pas les villes.")

if __name__ == "__main__":
    input_file = "cantons_et_villes_tries.json"
    output_file = "cantons_et_villes_geolocalises.json"
    add_geolocation(input_file, output_file)
