import json
import time
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Initialize geolocator with a user agent
geolocator = Nominatim(user_agent="swiss_cantons_cities")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)  # Add delay to respect API limits

def get_location(name):
    try:
        location = geocode(f"{name}, Switzerland")
        if location:
            return [location.latitude, location.longitude]
    except Exception as e:
        print(f"Error getting location for {name}: {e}")
    return [0, 0]  # Default coordinates if not found

def main():
    # Read cantons
    with open('canton.json', 'r', encoding='utf-8') as f:
        cantons = json.load(f)
    
    # Read cities
    with open('ville.json', 'r', encoding='utf-8') as f:
        cities = json.load(f)
    
    # Process each canton
    result = []
    
    for canton in cantons:
        canton_full = canton['nom_canton']
        canton_name = canton_full.split('—')[0].strip()
        canton_code = canton_full.split('—')[0].strip()  # Get the code part (e.g., 'ZH')
        
        # Get canton's geolocation
        canton_location = get_location(canton_name)
        
        # Filter cities for this canton
        canton_cities = []
        for city in cities:
            # Extract city name and canton code from city entry
            if '—' in city['nom_ville']:
                city_name, city_canton = map(str.strip, city['nom_ville'].rsplit('—', 1))
                if city_canton == canton_code:  # Match the canton code
                    canton_cities.append({
                        'nom_ville': city_name,
                        'geoLocation': get_location(f"{city_name}, {canton_name}, Switzerland")
                    })
        
        # Create canton entry
        canton_data = {
            'nomCanton': canton_name,
            'geoLocation': canton_location,
            'villeList': canton_cities,
            'VilleNombre': len(canton_cities)
        }
        
        result.append(canton_data)
        
        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)
    
    # Save the result
    with open('cantons_villes_geolocalisees.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print("Processing complete. Results saved to cantons_villes_geolocalisees.json")

if __name__ == "__main__":
    main()
