from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime
from PIL import Image
from bson import Binary, ObjectId
from bson.json_util import dumps
import os, io, requests

import config as c
import hash

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
def PUT_GET_DEL_image(db, coll, filename):
    
    # Check to see if db and collection exist
    try:
        db = cluster[db] # archives
        collection = db[coll] # tuscola, 404, etc.
    except:
        return f'Could not access {db} or {coll}\n', 400
        
    # Route to add a file into the specified db
    if request.method == 'PUT':
        try:
            # check if filename already exists
            cursor = collection.find_one({'filename': filename})
            if cursor:
                return f'File could not be added. Please rename {filename}\n', 400
                
            im = Image.open(f'./{filename}')
            image_bytes = io.BytesIO()
            im.save(image_bytes, format='JPEG')
            
            image_b = {'data': image_bytes.getvalue()}
            collection.insert_one({'filename': filename, 'image': image_b, 'UTC': datetime.now()}) 
            return jsonify({'image': image_b}), 200
        except:
            return f'{filename} could not be added\n', 400
        
    # Route to get a file from the specified db and collection
    if request.method == 'GET':
        try:
            cursor = collection.find_one({'filename': filename})
            image_b = cursor['image']['data']
            image = Image.open(io.BytesIO(image_b))
            image.save("image.jpg")
        except:
            return f'Could not find {filename}\n', 400       
        send_file(image)
        return f'{filename} found', 200
    
    # Route to delete a file from the specific db and collection
    if request.method == 'DELETE':
        try:
            collection.delete_one({'filename': filename})
            return f'Successfully deleted {filename} from {coll}\n', 200
        except:
            return 'File could not be deleted\n', 400
        
        
# Route to retrieve or delete all files in a specific collection
@app.route('/<db>/<coll>', methods=['GET', 'DELETE'])
def GET_images(db, coll):
    
    if request.method == 'GET':
        try:
            db = cluster[db] # archives
            collection = db[coll] # tuscola, 404, etc.
        except:
            return 'Could not access db or collection\n', 400
        
        cursor = collection.find({})
        images = []
        for item in cursor:
            with open(item['image'], 'rb') as image:         
                images.append(image)
        
        return jsonify({'images': images}), 200
    
    if request.method == 'DELETE':
        try:
            collection.delete_many({})
            return f'Successfully deleted all files in {coll}\n', 200
        except:
            return f'Files in {coll} could not be deleted\n', 400    

# TODO: fix video loop
# TODO: add button for archives page on index.html
# TODO: fix delete_one endpoint
# TODO: Figure out unique filenames when inserting them into mongo