"""Minimal ingestion helpers for orthomosaics and image metadata."""

from pathlib import Path

def list_images(folder):
    p = Path(folder)
    return [str(f) for f in p.iterdir() if f.suffix.lower() in ('.jpg', '.jpeg', '.tif', '.tiff', '.png')]


def sample_info(image_path):
    try:
        from detect_pits import _read_image
    except Exception:
        _read_image = None

    if _read_image:
        img, transform, crs = _read_image(image_path)
        return {'shape': img.shape, 'has_transform': transform is not None, 'crs': str(crs) if crs else None}
    else:
        return {'path': image_path}


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python ingest.py <images_folder>')
        raise SystemExit(1)
    imgs = list_images(sys.argv[1])
    for i in imgs[:10]:
        print(i, sample_info(i))
