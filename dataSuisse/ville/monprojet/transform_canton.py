import json

# Read the original JSON file
with open('canton.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Transform the data
transformed_data = []
for item in data:
    if '—' in item['nom_canton']:
        canton_code, canton_name = map(str.strip, item['nom_canton'].split('—', 1))
        transformed_data.append({
            'nom_canton': canton_name,
            'code': canton_code
        })

# Save the transformed data to a new file
with open('cantons_formatted.json', 'w', encoding='utf-8') as f:
    json.dump(transformed_data, f, ensure_ascii=False, indent=2)

print("Transformation complete. Results saved to cantons_formatted.json")
