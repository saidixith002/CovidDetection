# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 09:15:47 2022

@author: Sai dixith
"""

from flask import Flask
from flask import render_template

app=Flask(__name__)

@app.route('/')
def runhome():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')
'''
@app.route('/predict.html')
def predicthtml():
    return render_template('predict.html')
'''

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

app.secret_key = "secret key"
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/predict.html')
def upload_form():
	return render_template('predict.html')

from flask import request,flash,redirect,url_for
from werkzeug.utils import secure_filename
import os

@app.route('/predict.html', methods=['POST'])
def upload_image():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        return render_template('predict1.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

import cv2
from tensorflow.keras.models import load_model
model = load_model("M76.h5")

def loadModel():    
    return model

def predict(image):
    model = loadModel()
    img = cv2.resize(image, (180,180))
    import numpy as np
    img1 = np.reshape(img,(1,180,180,3))
    img1.shape
    result = model.predict(img1)
    total = np.sum(result)
   
    res = []
    for i in result[0]:
        res.append((i*100)/total)
    return res
def get_msg(l):
    msg = ''
    if(l[1] > 70):
        msg = 'Please consult the Doctor ASAP'
    elif(l[1]>40):
        msg = 'Has mild symptoms please take preventive measures'
    else:
        msg = 'You are absolutely fine. Please wear Mask'
        
    return msg

labels = ['Normal' , 'Covid']

@app.route('/main_prediction/<filename>')
def main_prediction(filename):
    #asda
    path = r'static\uploads'
    path = os.path.join(path,filename)    
    
    image = cv2.imread(path)
    outcome = predict(image)
    flash(get_msg(outcome))
    values = outcome
    return render_template('result.html', filename=filename, labels = labels, max= 110, values = values)
    
if __name__ == "__main__":
    app.run(debug=False)