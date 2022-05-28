from xml.dom.minidom import parseString
from PIL import Image
import pillow_heif
import os

# Helper to convert HEIC files to JPEG
# Removes original HEIC file from workspace
def heic_to_jpg(filename, dir):

    new_filename = filename
    
    if '.heif' not in filename:
        raise TypeError(f'\'{filename}\' was passed to heif.py but is not of HEIC format!')
    
    try:
        heif_file = pillow_heif.open_heif(f"{dir}/{filename}")
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
        
        new_filename = filename.split('.')[0]
        image.save(f"{dir}/{new_filename}.jpg", format("JPEG"))
        os.remove(f"{dir}/{filename}")
        
    except:
        pass
    
    return f'{new_filename}.jpg'