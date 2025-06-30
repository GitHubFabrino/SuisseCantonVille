import json

# Read the input JSON file
with open('cantons_et_villes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Sort cities within each canton alphabetically
for canton in data:
    if 'villeListe' in canton:
        canton['villeListe'] = sorted(canton['villeListe'], key=lambda x: x['nom_ville'])

# Sort cantons alphabetically by nom_canton
data_sorted = sorted(data, key=lambda x: x['nom_canton'])

# Save the sorted data to a new file
with open('cantons_et_villes_tries.json', 'w', encoding='utf-8') as f:
    json.dump(data_sorted, f, ensure_ascii=False, indent=2)

print("Sorting complete. Results saved to cantons_et_villes_tries.json")
