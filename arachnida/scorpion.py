from PIL import Image
import sys
import os
import time

allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

def get_image_metadata(file_path):

    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension not in allowed_extensions:
        print(f"\nUnsupported file type: {file_extension}")
        return
    if not os.path.exists(file_path):
        print(f"\nImage not found: {file_path}")
        return

    try: 
        image = Image.open(file_path)

        metadata = {
            "\nFile Name                  ": os.path.basename(file_path),
            "File Size                  ": os.path.getsize(file_path),
            "File Type                  ": image.format,
            "Image Width                ": image.width,
            "Image Height               ": image.height,
            "Has Color Map              ": image.info.get("background", None) is not None,
            "Color Resolution Depth     ": image.info.get("bits", None),
            "Comment                    ": image.info.get("comment", None),
            "Bits Per Pixel             ": image.info.get("bits", None),
            "Background Color           ": image.info.get("background", None),
            "Frame Count                ": getattr(image, 'n_frames', 1),
            "Duration                   ": image.info.get("duration", None),
            "Image Size                 ": f"{image.width}x{image.height}",
        }

        file_stat = os.stat(file_path)
        metadata.update({
            "File Modification Date/Time": time.ctime(file_stat.st_mtime),
            "File Access Date/Time      ": time.ctime(file_stat.st_atime),
        })
        for key, value in metadata.items():
            print(f"{key}: {value}")

    except Exception as e:
        print(f"\nScorpion ran into an Error processing image: {file_path}")
        print(e)

args = sys.argv[1:]

for arg in args:
    get_image_metadata(arg)

