from bson import _name_value_to_bson
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from PIL import Image
from bson.objectid import ObjectId
from bson.json_util import dumps
import os, io, requests, sys

import config as c
import hash
from image import get_byte_array, name_to_jpg

app = Flask(__name__)

import pymongo
cluster = pymongo.MongoClient(f"mongodb+srv://{c.username}:{c.pwd}@pilots.nvl9y.mongodb.net/Pilots?retryWrites=true&w=majority")




# route for "/" (frontend):
@app.route('/')
def index():
  return render_template("index.html")




# Route for the archives (frontend)
@app.route('/gallery')
def GET_gallery():
    return render_template("gallery.html")




# Route for returning a specific image
@app.route('/images/image-<x>.jpg', methods=['GET'])
def GET_image(x):
    return send_file(f'images/image-{x}.jpg')




# Route for returning the space background video
@app.route('/space.mp4', methods=['GET'])
def GET_video():
    return send_file(f'templates/space.mp4')
  



# Routes to retrieve, insert or delete a specified file
@app.route('/<db>/<coll>/<filename>', methods=['PUT', 'GET', 'DELETE'])
def single_file(db, coll, filename):
    
    # Check to see if db and collection exist
    try:
        database = cluster[db] # archives
        collection = database[coll] # tuscola, 404, etc.
    except:
        return f'Could not access {db} or {coll}\n', 400
    
        
    # Route to add a file into the specified db
    if request.method == 'PUT': 

        fname_as_jpg = name_to_jpg(filename)
        
        try:
            # Check if filename (as .jpg) already exists
            cursor = collection.find_one({'filename': fname_as_jpg})
            if cursor:
                return f'File could not be added. Please rename {filename}\n', 400
                
            image_b = get_byte_array()
            
            collection.insert_one({'filename': str(fname_as_jpg), 'image': image_b, 'UTC': datetime.now()}) 
            return f'Successfully added {fname_as_jpg} to collection \'{coll}\' in database \'{db}\'', 200
        except:
            return f'{filename} could not be added\n', 400
        
        
    # Route to get a file from the specified db and collection
    if request.method == 'GET':
        
        try:
            cursor = collection.find_one({'filename': filename})
            image_b = cursor['image']['data']
            image = Image.open(io.BytesIO(image_b))
            image.save(f'{db}/{coll}/{filename}')  
        except:
            return f'Could not find {filename}\n', 400    
           
        return send_file(f'{db}/{coll}/{filename}'), 200
    
    
    # Route to delete a file from the specific db and collection
    if request.method == 'DELETE':
        
        try:
            collection.delete_one({'filename': str(filename)})
            return f'Successfully deleted {filename} from {coll}\n', 200
        except:
            return 'File could not be deleted\n', 400
 
 
        
        
# Route to retrieve or delete all files in a specific collection
# 'CLEAR' endpoint deletes all local files in the specified db/coll directory
# 'PUT' endpoint adds an entire local folder to the collection
@app.route('/<db>/<coll>', methods=['GET', 'DELETE', 'CLEAR', 'PUT'])
def multiple_files(db, coll):
    
    # Check to see if db and collection exist
    try:
        database = cluster[db] # archives
        collection = database[coll] # tuscola, 404, etc.
    except:
        return f'Could not access {db} or {coll}\n', 400
   
    
    if request.method == 'GET':
        
        cursor = collection.find({})
        filenames = []
        
        for item in cursor:
            
            f_name = str(item['filename']).strip()
            filenames.append(f_name)
            image = Image.open(io.BytesIO(item['image']['data']))
            image.save(f'{db}/{coll}/{f_name}')
        
        return jsonify({"filenames": filenames}), 200
   
    
    if request.method == 'DELETE':
        
        try:
            collection.delete_many({})
            return f'Successfully deleted all files in {coll}\n', 200
        
        except:
            return f'Files in {coll} could not be deleted\n', 400
        
        
    if request.method == 'CLEAR':
        
        dir = f'{db}/{coll}'
        try:
            
            for filename in os.listdir(dir):
            
                f = os.path.join(dir, filename)
                os.remove(f)
            
            return f'Cleared {db}/{coll} directory\n', 200
        
        except:
            return f'Could not clear {db}/{coll} directory\n', 400
        
        
    if request.method == 'PUT':
        
        dir = f'local/{db}/{coll}'
        output_msg = ""
        file_count = 0
        
        for filename in os.listdir(dir):
            
                fname_as_jpg = name_to_jpg(filename)

                # check if filename already exists
                # if it does, add it to a list of filenames that need to be renamed
                cursor = collection.find_one({'filename': fname_as_jpg})
                if cursor:
                    output_msg = output_msg + f'The name \'{fname_as_jpg}\' already exists in the collection\n'
                    continue
                
                image_b = get_byte_array(filename, dir)
                
                collection.insert_one({'filename': str(fname_as_jpg), 'image': image_b, 'UTC': datetime.now()})
                file_count += 1
                
        if file_count == 0 and len(output_msg) == 0:
            return 'Local directory may be empty!', 400
        
        elif len(output_msg) == 0: 
            return f'Successfully added all {file_count} files', 200
        
        else:
            return f'Successfully added {file_count} files\nBut there were errors with the following files:\n{output_msg}', 200






# TODO: fix video loop
# TODO: fix delete_one endpoint
# TODO: Create loading circle animation in archives
# TODO: Pick a few images for static initial load of each archive page
