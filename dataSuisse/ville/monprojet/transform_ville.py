import json

# Read the original JSON file
with open('ville.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Transform the data
transformed_data = []
for item in data:
    if '—' in item['nom_ville']:
        city_name, city_code = map(str.strip, item['nom_ville'].rsplit('—', 1))
        transformed_data.append({
            'nom_ville': city_name,
            'code': city_code
        })

# Save the transformed data to a new file
with open('villes_formatted.json', 'w', encoding='utf-8') as f:
    json.dump(transformed_data, f, ensure_ascii=False, indent=2)

print("Transformation complete. Results saved to villes_formatted.json")
