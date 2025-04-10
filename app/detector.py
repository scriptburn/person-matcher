from PIL import Image
import os
from pathlib import Path

def detect_and_crop(image_path, crop_prefix="crop", output_dir="crops"):
    # Simulated detection (replace with actual YOLO/whatever)
    img = Image.open(image_path)
    width, height = img.size

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    crop_path = f"{output_dir}/{crop_prefix}_0.jpg"
    img.save(crop_path)

    return [{
        "crop_path": crop_path,
        "bbox": [0, 0, width, height]
    }]