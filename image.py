from PIL import Image
import pillow_heif
import os, io


# Helper to convert HEIC files to JPEG
# Creates a deep copy in JPEG format
# Removes original HEIC file from workspace
def heic_to_jpg(filename, dir):

    new_filename = name_to_jpg(filename)
    
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
        
        image.save(f"{dir}/{new_filename}", format("JPEG"))
        os.remove(f"{dir}/{filename}")
        
    except:
        raise Exception(f'Could not convert {filename} to {new_filename}')
    
    return new_filename



# Helper for both PUT endpoints
# Returns the byte array of the image to be inserted
def get_byte_array(filename, dir):
    
    # If current file is in HEIC format, convert to JPEG
    if '.heif' in filename:
        new_filename = heic_to_jpg(filename, dir)
    else:
        new_filename = name_to_jpg(filename)
        
    try:
        im = Image.open(f'{dir}/{new_filename}')
        image_bytes = io.BytesIO()
        im.save(image_bytes, format='JPEG')
        
        image_b = {'data': image_bytes.getvalue()}
        
        return image_b
    except:
        raise Exception(f'Could not get byte array for {filename}')



# Helper to rename a file to in .jpg
# changes ONLY the name, does not change actual file
def name_to_jpg(filename):
    
    new_filename = filename # 'IMG_123.heif'
    
    parts = filename.split('.') # ['IMG_123', 'heif']
    name = parts[0] # 'IMG_123'
    type = parts[1] # 'heif'
    
    if type != 'jpg':
        new_filename = f'{name}.jpg'
    
    return new_filename # 'IMG_123.jpg'
