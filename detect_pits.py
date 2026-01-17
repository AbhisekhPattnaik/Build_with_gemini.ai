"""Pit detection prototype.

Usage:
    from detect_pits import detect_pits
    detect_pits('orthomosaic.tif', 'out.pits.geojson')

The detector uses a Laplacian / blob detector on a grayscale image
to find circular dark spots (pits). If the input is a GeoTIFF and
`rasterio` is available, output GeoJSON coordinates are in the image CRS.
Otherwise pixel coordinates are written.
"""

from pathlib import Path
import json
import numpy as np
import cv2

try:
    import rasterio
    from rasterio.transform import Affine
    HAS_RASTERIO = True
except Exception:
    HAS_RASTERIO = False

from skimage.feature import blob_log
from skimage.feature import blob_dog
from skimage.filters import gaussian


def _read_image(path):
    path = Path(path)
    if HAS_RASTERIO and path.suffix.lower() in ('.tif', '.tiff'):
        ds = rasterio.open(str(path))
        arr = ds.read()
        # rasterio returns (bands, rows, cols) -> transpose to (rows, cols, bands)
        img = np.transpose(arr, (1, 2, 0))
        transform = ds.transform
        crs = ds.crs
        return img, transform, crs
    # fallback to cv2
    img = cv2.imread(str(path))
    return img, None, None


def detect_pits(image_path, out_geojson=None, min_sigma=3, max_sigma=12, num_sigma=8, threshold=0.02):
    img, transform, crs = _read_image(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    # convert to grayscale float
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    gray = gray.astype(float) / 255.0

    # enhance dark circular pits: use Laplacian of Gaussian via blob_log
    blobs = blob_log(gray, min_sigma=min_sigma, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)
    # blob_log returns (y, x, sigma)

    features = []
    for y, x, sigma in blobs:
        radius = sigma * np.sqrt(2)
        if transform is not None:
            # rasterio transform expects row, col (y, x)
            col = int(round(x))
            row = int(round(y))
            px, py = rasterio.transform.xy(transform, row, col)
            coord = [px, py]
        else:
            coord = [float(x), float(y)]

        properties = {"radius_px": float(radius)}
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coord},
            "properties": properties,
        })

    fc = {"type": "FeatureCollection", "features": features}

    if out_geojson:
        with open(out_geojson, 'w', encoding='utf8') as fh:
            json.dump(fc, fh, indent=2)

    return fc


def detect_cleared_areas(image_path, out_geojson=None, min_sigma=5, max_sigma=30, num_sigma=10, threshold=0.02):
    """Detect likely cleared (bare soil) circular areas (OP3) by finding bright/non-green circular blobs.

    Returns GeoJSON FeatureCollection of detected centers and radius_px.
    """
    img, transform, crs = _read_image(image_path)
    if img is None:
        raise FileNotFoundError(f"Cannot read image: {image_path}")

    # Convert to HSV and build a 'non-green' brightness image
    if img.ndim == 3:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Value channel highlights bright soil
        val = hsv[:, :, 2].astype(float) / 255.0
        # mask green areas to down-weight vegetation
        lower = np.array([30, 30, 30])
        upper = np.array([90, 255, 255])
        green_mask = cv2.inRange(hsv, lower, upper).astype(bool)
        # create an image where bare soil = bright and vegetation suppressed
        soil_like = val.copy()
        soil_like[green_mask] = soil_like[green_mask] * 0.2
    else:
        soil_like = img.astype(float) / 255.0

    # Smooth and detect blobs (bright spots)
    soil_smooth = gaussian(soil_like, sigma=1)
    blobs = blob_log(soil_smooth, min_sigma=min_sigma, max_sigma=max_sigma, num_sigma=num_sigma, threshold=threshold)

    features = []
    for y, x, sigma in blobs:
        radius = sigma * np.sqrt(2)
        if transform is not None:
            col = int(round(x))
            row = int(round(y))
            px, py = rasterio.transform.xy(transform, row, col)
            coord = [px, py]
        else:
            coord = [float(x), float(y)]

        properties = {"radius_px": float(radius)}
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coord},
            "properties": properties,
        })

    fc = {"type": "FeatureCollection", "features": features}
    if out_geojson:
        with open(out_geojson, 'w', encoding='utf8') as fh:
            json.dump(fc, fh, indent=2)
    return fc


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python detect_pits.py <image> [out.geojson]")
        sys.exit(1)
    img = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) >= 3 else None
    fc = detect_pits(img, out)
    print(f"Detected {len(fc['features'])} candidate pits.")
