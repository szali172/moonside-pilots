from flask import Flask, render_template, request, jsonify, send_file
import requests
from datetime import datetime
import os

app = Flask(__name__)

from pymongo import MongoClient
mongo = MongoClient('localhost', 27017)
db = mongo["pilots-db"]


# route for "/" (frontend):
@app.route('/')
def index():
  return render_template("index.html")

@app.route('/gallery')
def GET_gallery():
    return render_template("gallery.html")

@app.route('/images/image-<x>.jpg', methods=['GET'])
def GET_image(x):
    return send_file(f'images/image-{x}.jpg')
