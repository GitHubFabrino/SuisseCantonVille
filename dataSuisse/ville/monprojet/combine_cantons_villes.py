import json

# Load the formatted cantons and cities
with open('cantons_formatted.json', 'r', encoding='utf-8') as f:
    cantons = json.load(f)

with open('villes_formatted.json', 'r', encoding='utf-8') as f:
    villes = json.load(f)

# Create a dictionary to map canton codes to their data
canton_map = {canton['code']: {
    'nom_canton': canton['nom_canton'],
    'villeListe': [],
    'code': canton['code'],
    'villeNombre': 0
} for canton in cantons}

# Group cities by canton
for ville in villes:
    code = ville['code']
    if code in canton_map:
        canton_map[code]['villeListe'].append({
            'nom_ville': ville['nom_ville']
        })

# Update the count of cities for each canton
for code in canton_map:
    canton_map[code]['villeNombre'] = len(canton_map[code]['villeListe'])

# Convert the dictionary to a list
result = list(canton_map.values())

# Save the result to a new file
with open('cantons_et_villes.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Combination complete. Results saved to cantons_et_villes.json")
