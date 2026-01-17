import json
import sys

if len(sys.argv) < 2:
    print('Usage: python count_geojson_features.py file.geojson')
    raise SystemExit(1)

path = sys.argv[1]
with open(path, 'r', encoding='utf8') as fh:
    fc = json.load(fh)
print(len(fc.get('features',[])))
