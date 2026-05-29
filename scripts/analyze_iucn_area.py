import csv
from collections import defaultdict

input_file = 'DV2/data/capad_metadata.csv'
area_sums = defaultdict(float)
counts = defaultdict(int)

with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cat = row['IUCN']
        try:
            area = float(row['GIS_AREA']) if row['GIS_AREA'] else 0
            area_sums[cat] += area
            counts[cat] += 1
        except ValueError:
            pass

print("IUCN Category | Count | Total Area (ha)")
print("-" * 40)
for cat in sorted(area_sums.keys()):
    print(f"{cat:13} | {counts[cat]:5} | {area_sums[cat]:,.2f}")
