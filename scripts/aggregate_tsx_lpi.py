import csv
import math
from collections import defaultdict

input_file = 'DV2/data/tsx-aggregated-data-dataset=tsx2025&type=all&tgroup=All&group=All&subgroup=All&state=All&statusauth=Max&status=NT_VU_EN_CR&management=All&refyear=1985.csv'
output_file = 'DV2/data/tsx_index_actual.csv'

years = [str(y) for y in range(1985, 2023)]
groups = ['Birds', 'Amphibians', 'Mammals', 'Plants', 'Reptiles']

# group_year_rates[group][year_interval] = list of r values
group_year_rates = defaultdict(lambda: defaultdict(list))

print(f"Processing {input_file} using Geometric Mean method...")

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        group = row['TaxonomicGroup']
        if group not in groups:
            continue
            
        for i in range(len(years) - 1):
            y_curr = years[i]
            y_next = years[i+1]
            
            val_curr_str = row[y_curr]
            val_next_str = row[y_next]
            
            if val_curr_str and val_next_str:
                try:
                    v_curr = float(val_curr_str)
                    v_next = float(val_next_str)
                    
                    if v_curr > 0 and v_next > 0:
                        # r = log(v_next / v_curr)
                        r = math.log(v_next / v_curr)
                        group_year_rates[group][y_next].append(r)
                except ValueError:
                    pass

print("Rates calculated. Generating Index...")

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Group', 'Relative_Abundance'])
    
    for group in groups:
        # Start at 1.0 in 1985
        current_index = 1.0
        writer.writerow(['1985', group, 1.0])
        
        for y in years[1:]:
            rates = group_year_rates[group][y]
            if rates:
                avg_r = sum(rates) / len(rates)
                current_index = current_index * math.exp(avg_r)
                writer.writerow([y, group, round(current_index, 4)])

print(f"LPI-style index saved to {output_file}")
