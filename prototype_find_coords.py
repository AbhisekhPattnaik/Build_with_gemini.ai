"""Prototype to find OP1 (pits) and OP3 (cleared areas) coordinates across folders.

Usage:
    python prototype_find_coords.py --op1_folder path/to/op1_tiles --op3_folder path/to/op3_tiles --out_dir out

The script will process all image files in the given folders, run `detect_pits`
on OP1 tiles and `detect_cleared_areas` on OP3 tiles, and write merged GeoJSONs
`op1_pits.geojson` and `op3_cleared.geojson` to `out_dir`.
"""

import argparse
from pathlib import Path
import json
import re
from detect_pits import detect_pits, detect_cleared_areas


def list_img_files(folder):
    p = Path(folder)
    return sorted([str(f) for f in p.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.png', '.tif', '.tiff')])


def merge_feature_collections(fc_list):
    features = []
    for fc in fc_list:
        features.extend(fc.get('features', []))
    return {'type': 'FeatureCollection', 'features': features}


def run_folder(folder, detector, out_geojson):
    files = list_img_files(folder)
    fcs = []
    for f in files:
        try:
            fc = detector(f)
        except Exception as e:
            print('Error processing', f, e)
            continue

        # If detector returned pixel coords (tile-local), compute global pixel coords
        # by parsing tile filename for origin offsets like '_V_<ox>_<oy>'.
        m = re.search(r'_V_(\d+)_(\d+)', Path(f).name)
        origin_x = int(m.group(1)) if m else 0
        origin_y = int(m.group(2)) if m else 0

        for feat in fc.get('features', []):
            coord = feat.get('geometry', {}).get('coordinates', [None, None])
            if coord is None:
                continue
            # If the detector gave geographic coords (likely floats large or with decimals), skip global pixel math
            # Heuristic: if origin present and coords look like small pixel values (e.g., <= 5000), add origin
            try:
                x_c = float(coord[0])
                y_c = float(coord[1])
            except Exception:
                continue

            if m and max(x_c, y_c) < 10000:
                feat.setdefault('properties', {})['tile_origin'] = [origin_x, origin_y]
                feat.setdefault('properties', {})['local_px'] = [x_c, y_c]
                feat.setdefault('properties', {})['global_px'] = [origin_x + x_c, origin_y + y_c]
            else:
                # keep as-is; add crs_coord if present
                feat.setdefault('properties', {})['crs_coord'] = [x_c, y_c]

        fcs.append(fc)

    merged = merge_feature_collections(fcs)
    with open(out_geojson, 'w', encoding='utf8') as fh:
        json.dump(merged, fh, indent=2)
    print('Wrote', out_geojson, 'features:', len(merged['features']))
    return merged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--op1_folder', required=True)
    ap.add_argument('--op3_folder', required=True)
    ap.add_argument('--out_dir', required=True)
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    op1_out = out_dir / 'op1_pits.geojson'
    op3_out = out_dir / 'op3_cleared.geojson'

    print('Processing OP1 (pits) in', args.op1_folder)
    run_folder(args.op1_folder, detect_pits, str(op1_out))

    print('Processing OP3 (cleared areas) in', args.op3_folder)
    run_folder(args.op3_folder, detect_cleared_areas, str(op3_out))


if __name__ == '__main__':
    main()
