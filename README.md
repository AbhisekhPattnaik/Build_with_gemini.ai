# Afforestation PoC - Drone-based sapling survival

This repository contains a small proof-of-concept pipeline to:

- detect pits (OP1) from an orthomosaic (`detect_pits.py`)
- provide simple ingestion helpers (`ingest.py`)
- a heuristic classifier for presence/absence (`classify.py`)
- a CLI entrypoint `estimatesurvival.py` to run detection and export GeoJSON

Quick start:

1. Install dependencies (recommend inside a virtualenv):

```bash
python -m pip install -r requirements.txt
```

2. Run pit detection on an orthomosaic:

```bash
python estimatesurvival.py path/to/orthomosaic.tif out.pits.geojson
```

Next steps:
- improve pit detector and tune blob parameters for your imagery
- implement robust alignment between epochs using feature matches
- build a classifier (CNN or classic) trained on cropped patches
- evaluate against the ground-truth dead sapling coordinates
