import csv
from collections import defaultdict

input_file = 'DV2/data/tsx-aggregated-data-dataset=tsx2025&type=all&tgroup=All&group=All&subgroup=All&state=All&statusauth=Max&status=NT_VU_EN_CR&management=All&refyear=1985.csv'
output_file = 'DV2/data/tsx_index_actual.csv'

years = [str(y) for y in range(1985, 2023)]
groups = ['Birds', 'Amphibians', 'Mammals', 'Plants', 'Reptiles']

# species_year_sums[group][species][year]
species_year_sums = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
# species_year_counts[group][species][year]
species_year_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

print(f"Processing {input_file}...")

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        group = row['TaxonomicGroup']
        species = row['Binomial']
        if group not in groups:
            continue
            
        for year in years:
            val_str = row[year]
            if val_str:
                try:
                    val = float(val_str)
                    species_year_sums[group][species][year] += val
                    species_year_counts[group][species][year] += 1
                except ValueError:
                    pass

print("Species-level aggregation complete. Calculating group indices...")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Group', 'Relative_Abundance'])
    
    for group in groups:
        # group_year_rel_sums[year]
        group_year_rel_sums = defaultdict(float)
        # group_year_rel_counts[year]
        group_year_rel_counts = defaultdict(int)
        
        for species in species_year_sums[group]:
            # Calculate species baseline (average in 1985)
            s_baseline_sum = species_year_sums[group][species]['1985']
            s_baseline_count = species_year_counts[group][species]['1985']
            
            if s_baseline_count > 0:
                s_baseline = s_baseline_sum / s_baseline_count
                if s_baseline > 0:
                    for year in years:
                        if species_year_counts[group][species][year] > 0:
                            s_avg = species_year_sums[group][species][year] / species_year_counts[group][species][year]
                            s_rel = s_avg / s_baseline
                            group_year_rel_sums[year] += s_rel
                            group_year_rel_counts[year] += 1
        
        for year in years:
            if group_year_rel_counts[year] > 0:
                idx = group_year_rel_sums[year] / group_year_rel_counts[year]
                writer.writerow([year, group, round(idx, 4)])

print(f"Final aggregated data saved to {output_file}")
