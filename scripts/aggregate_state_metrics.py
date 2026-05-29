import csv
import os

input_file = 'DV2/data/capad_metadata.csv'
output_file = 'DV2/data/state_gap_metrics.csv'

# State land areas in Hectares
state_land_areas = {
    'VIC': 22741600,
    'NSW': 80064200,
    'QLD': 173064800,
    'SA': 98348200,
    'WA': 252987500,
    'TAS': 6840100,
    'NT': 134912900,
    'ACT': 235800
}

state_names = {
    'VIC': 'Victoria',
    'NSW': 'New South Wales',
    'QLD': 'Queensland',
    'SA': 'South Australia',
    'WA': 'Western Australia',
    'TAS': 'Tasmania',
    'NT': 'Northern Territory',
    'ACT': 'Australian Capital Territory'
}

# Initialize data structures
state_data = {
    state: {
        'terrestrial_area_sum': 0.0,
        'terrestrial_count': 0,
        'marine_area_sum': 0.0,
        'marine_count': 0
    }
    for state in state_land_areas
}

print(f"Reading from {input_file}...")
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        state = row['STATE']
        # Map some standard variants if needed
        if state not in state_data:
            continue
        
        try:
            area = float(row['GIS_AREA'])
        except (ValueError, TypeError):
            continue
            
        environ = row['ENVIRON']
        
        if environ == 'T':
            state_data[state]['terrestrial_area_sum'] += area
            state_data[state]['terrestrial_count'] += 1
        elif environ == 'M':
            state_data[state]['marine_area_sum'] += area
            state_data[state]['marine_count'] += 1

print("Calculating aggregated metrics...")
output_rows = []
for state, data in state_data.items():
    # 1. Terrestrial Area %
    land_area = state_land_areas[state]
    terr_sum = data['terrestrial_area_sum']
    terr_percent = (terr_sum / land_area) * 100
    
    # 2. Mean Terrestrial Size
    terr_count = data['terrestrial_count']
    mean_terr_size = (terr_sum / terr_count) if terr_count > 0 else 0
    
    # 3. Marine Sum
    marine_sum = data['marine_area_sum']
    marine_count = data['marine_count']
    mean_marine_size = (marine_sum / marine_count) if marine_count > 0 else 0
    
    row = {
        'STATE': state,
        'STATE_NAME': state_names[state],
        'Land_Area_ha': land_area,
        'Terrestrial_Protected_ha': round(terr_sum, 2),
        'Terrestrial_Protected_Percent': round(terr_percent, 2),
        'Terrestrial_Count': terr_count,
        'Mean_Terrestrial_Size_ha': round(mean_terr_size, 2),
        'Marine_Protected_ha': round(marine_sum, 2),
        'Marine_Count': marine_count,
        'Mean_Marine_Size_ha': round(mean_marine_size, 2)
    }
    output_rows.append(row)

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write to output file
fields = ['STATE', 'STATE_NAME', 'Land_Area_ha', 'Terrestrial_Protected_ha', 'Terrestrial_Protected_Percent', 'Terrestrial_Count', 'Mean_Terrestrial_Size_ha', 'Marine_Protected_ha', 'Marine_Count', 'Mean_Marine_Size_ha']
print(f"Writing to {output_file}...")
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(output_rows)

print("Aggregation completed successfully!")
