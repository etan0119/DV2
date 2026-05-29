import csv
import os

input_file = 'DV2/data/tsx-aggregated-data-dataset=tsx2025&type=all&tgroup=All&group=All&subgroup=All&state=All&statusauth=Max&status=NT_VU_EN_CR&management=All&refyear=1985.csv'
output_file = 'DV2/data/tsx_management_gap.csv'

print(f"Reading species data from {input_file}...")
species_managements = {}

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['EPBCStatus']:
            continue
            
        group = row['TaxonomicGroup']
        mgmt = row['Management']
        binomial = row['Binomial']
        
        if not group or not mgmt or not binomial:
            continue
            
        if binomial not in species_managements:
            species_managements[binomial] = {
                'group': group,
                'managements': set()
            }
        species_managements[binomial]['managements'].add(mgmt)

# Calculate mutually exclusive categories
# 1. Actively Managed: only 'Actively managed'
# 2. Partially Managed: both 'Actively managed' and 'No known management'
# 3. No Known Management: only 'No known management'
group_counts = {}
for binomial, info in species_managements.items():
    group = info['group']
    managements = info['managements']
    
    if managements == {'Actively managed'}:
        cat = 'Actively Managed'
    elif managements == {'Actively managed', 'No known management'}:
        cat = 'Partially Managed'
    else:
        cat = 'No Known Management'
        
    if group not in group_counts:
        group_counts[group] = {
            'Actively Managed': 0,
            'Partially Managed': 0,
            'No Known Management': 0,
            'Total': 0
        }
    group_counts[group][cat] += 1
    group_counts[group]['Total'] += 1

# Prepare output rows
output_rows = []
print("Preparing aggregated rows...")
for group, counts in group_counts.items():
    total = counts['Total']
    for cat in ['Actively Managed', 'Partially Managed', 'No Known Management']:
        count = counts[cat]
        percentage = (count / total) * 100 if total > 0 else 0
        
        row = {
            'TaxonomicGroup': group,
            'Management': cat,
            'Species_Count': count,
            'Total_Species_Group': total,
            'Percentage': round(percentage, 2)
        }
        output_rows.append(row)

# Ensure output directory exists
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Write to CSV
fields = ['TaxonomicGroup', 'Management', 'Species_Count', 'Total_Species_Group', 'Percentage']
print(f"Saving mutually exclusive data to {output_file}...")
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    writer.writerows(output_rows)

print("Management gap data generation completed successfully!")
