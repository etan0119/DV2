import json
import csv
import os

input_file = 'DV2/topojson/CAPAD-full.json'
output_file = 'DV2/data/capad_metadata.csv'

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

print(f"Opening {input_file}...")
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# TopoJSON structure: objects -> [layer_name] -> geometries
# Based on the previous read, it seems the main object is under 'objects'
# Let's find the key inside 'objects'
objects_key = list(data['objects'].keys())[0]
geometries = data['objects'][objects_key]['geometries']

print(f"Found {len(geometries)} geometries. Extracting properties...")

# Fields we want to keep
fields = ['NAME', 'TYPE', 'TYPE_ABBR', 'IUCN', 'GAZ_AREA', 'GIS_AREA', 'GAZ_DATE', 'STATE', 'AUTHORITY', 'ENVIRON', 'LONGITUDE', 'LATITUDE', 'PA_SYSTEM']

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for geom in geometries:
        props = geom.get('properties', {})
        # Create a filtered dict with only the fields we want
        row = {field: props.get(field) for field in fields}
        writer.writerow(row)

print(f"Successfully saved metadata to {output_file}")
