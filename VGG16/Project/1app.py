from keras.applications import VGG16
from keras.applications.vgg16 import preprocess_input
from keras.preprocessing import image
from keras.models import Model

import numpy as np
import pandas as pd

from IPython.display import Image
from os import listdir as ld

#이미지를 불러오기 위해 필요한 package
import keras.utils as utils

from flask import Flask, send_file, render_template


app = Flask(__name__)


@app.route('/')
def home():
    img_url = "C:\\Users\\admin\\Desktop\\Github\\Final-Project\\VGG16\\Project\\static\\img\\main.jpg"
    return render_template('main.html', main_Img = img_url)


@app.route('/vgg16')
def vgg16():
    
    vgg_model = VGG16(weights='imagenet', include_top=False)
    model = Model(inputs=vgg_model.input, outputs=vgg_model.get_layer('block5_pool').output)
    
    img1 = utils.load_img("C:\\Users\\admin\\Desktop\\Github\\Final-Project\\VGG16\\Project\\static\\img\\main.jpg", target_size=(224, 224))
    img1 = utils.img_to_array(img1)
    img1 = np.expand_dims(img1, axis=0)
    img1 = preprocess_input(img1)
    features1 = model.predict(img1)
    features1 = features1.flatten()
    
    
    img2 = utils.load_img("C:\\Users\\admin\\Desktop\\Github\\Final-Project\\VGG16\\Project\\static\\img\\0.jpg", target_size=(224, 224))
    img2 = utils.img_to_array(img2)
    img2 = np.expand_dims(img2, axis=0)
    img2 = preprocess_input(img2)
    features2 = model.predict(img2)
    features2 = features2.flatten()
    
    cosine_similarity = np.dot(features1, features2) / (np.linalg.norm(features1) * np.linalg.norm(features2))
    print("Cosine similarity: ", cosine_similarity)
    
    
    img_String = ''
    if cosine_similarity > 0.3 :
        img_String = '유사합니다.'
    else :
        img_String = '유사하지 않습니다.'
        
    
    return render_template('main.html', img_answer = img_String, cos = cosine_similarity)



if __name__ == '__main__' :
    app.run(debug=True)


