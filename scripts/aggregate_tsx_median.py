import csv
from collections import defaultdict
import statistics

input_file = 'DV2/data/tsx-aggregated-data-dataset=tsx2025&type=all&tgroup=All&group=All&subgroup=All&state=All&statusauth=Max&status=NT_VU_EN_CR&management=All&refyear=1985.csv'
output_file = 'DV2/data/tsx_index_actual.csv'

years = [str(y) for y in range(1985, 2023)]
groups = ['Birds', 'Amphibians', 'Mammals', 'Plants', 'Reptiles']

# Store lists of relative abundance for each (group, year)
relative_values = defaultdict(list)

print(f"Processing {input_file}...")

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        group = row['TaxonomicGroup']
        if group not in groups:
            continue
        
        # Get baseline (1985). If not available, skip this series
        try:
            baseline = float(row['1985']) if row['1985'] and float(row['1985']) > 0 else None
        except ValueError:
            baseline = None
            
        if baseline is None:
            continue
            
        for year in years:
            val_str = row[year]
            if val_str:
                try:
                    val = float(val_str)
                    rel_val = val / baseline
                    relative_values[(group, year)].append(rel_val)
                except ValueError:
                    pass

print("Calculation complete. Saving results...")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Group', 'Relative_Abundance'])
    for group in groups:
        for year in years:
            vals = relative_values[(group, year)]
            if vals:
                # Use median to avoid outlier skew
                med_rel = statistics.median(vals)
                writer.writerow([year, group, round(med_rel, 4)])

print(f"Aggregated data saved to {output_file}")
