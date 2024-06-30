
from flask import Flask,request,render_template
import os
import tensorflow as tf
from flask import Flask,render_template,request
from PIL import Image
import requests



app = Flask(__name__)
model = tf.keras.models.load_model("Aircraft.h5")


@app.route('/')
def hello_world():
    return render_template('index.html')



@app.route('/choose')
def choose():
    return render_template('choose.html')



@app.route('/predict', methods=['POST'])
def upload_image():

    if 'image' not in request.files:
        return "No file part"
    
    image = request.files['image']
    
    if image.filename == '':
        return "No selected file"
    

    upload_path = os.path.join('static/images', image.filename)
    image.save(upload_path)
    img = Image.open(upload_path).resize((224, 224))  
    image_array = tf.keras.preprocessing.image.img_to_array(img)  
    image_array = tf.expand_dims(image_array, 0)



    prediction = model.predict(image_array)

    if prediction[0][0] >= 0.5:
        return render_template('model.html',image_source=upload_path,res="Defective")
    else:
        return render_template('model.html',image_source=upload_path,res="Non-Defective")


if __name__ == '__main__':
    app.run(debug=True)




