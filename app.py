# app.py
from LumenObj import ImageLuminanceAnalyzer
from flask import Flask, request, jsonify
import json

app = Flask(__name__)

from PIL import Image

@app.route('/writeToFile', methods=['POST'])
def processImage():
    image = request.files['image']
    # Open the image file using Pillow
    image = Image.open(image.stream)
    imageProcess = ImageLuminanceAnalyzer(image)
    # rest of your code...
    if 'image' not in request.files:
        print("error 0")
        return 'No image part in the request', 400
    
    if 'location' not in request.form:
        print("error 1")
        return 'No Location', 400
    if 'time' not in request.form:
        print("error 2")
        return 'no time', 400
    
    image = request.files['image']
    location = request.form['location']
    
    if 'time' in request.form:
        time = request.form['time']
        if time not in ['Morning', 'Afternoon']:
            time = "null"
    else:
        time = "null"

    imageProcess = ImageLuminanceAnalyzer(image)
    light = imageProcess.getLightLevel()

    data = {
        'light': light,
        'location': location,
        'time': time
    }

    with open('map.json', 'a') as file:
        json.dump(data, file)
        file.write('\n')  # add a newline after each JSON object

    return jsonify(message='Success'), 200

if __name__ == '__main__':
    app.run(port=5000)