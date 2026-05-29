import csv
from collections import defaultdict

input_file = 'DV2/data/tsx-aggregated-data-dataset=tsx2025&type=all&tgroup=All&group=All&subgroup=All&state=All&statusauth=Max&status=NT_VU_EN_CR&management=All&refyear=1985.csv'
output_file = 'DV2/data/tsx_index_actual.csv'

years = [str(y) for y in range(1985, 2023)]
groups = ['Birds', 'Amphibians', 'Mammals', 'Plants', 'Reptiles']

# Store sum of values for each (group, year)
total_sums = defaultdict(float)

print(f"Processing {input_file}...")

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        group = row['TaxonomicGroup']
        if group not in groups:
            continue
            
        for year in years:
            val_str = row[year]
            if val_str:
                try:
                    val = float(val_str)
                    total_sums[(group, year)] += val
                except ValueError:
                    pass

print("Calculation complete. Saving results...")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Group', 'Relative_Abundance'])
    for group in groups:
        # Get baseline sum (1985)
        baseline_sum = total_sums[(group, '1985')]
        if baseline_sum <= 0:
            # If 1985 is 0, find the first non-zero year as baseline
            for y in years:
                if total_sums[(group, y)] > 0:
                    baseline_sum = total_sums[(group, y)]
                    break
        
        if baseline_sum > 0:
            for year in years:
                current_sum = total_sums[(group, year)]
                rel_abun = current_sum / baseline_sum
                writer.writerow([year, group, round(rel_abun, 4)])

print(f"Aggregated data saved to {output_file}")
