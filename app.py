from flask import Flask, render_template, request
import os
from stegano import encode_message, decode_message
from werkzeug.utils import secure_filename
import time

app = Flask(__name__)
UPLOAD_FOLDER = 'static/images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    file = request.files['image']
    message = request.form['message']

    if not file or not message:
        return "Please upload an image and provide a message."

    filename = secure_filename(file.filename)
    unique_filename = f"{int(time.time())}_{filename}"
    image_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(image_path)

    output_filename = f"encoded_{unique_filename}"
    output_path = os.path.join(UPLOAD_FOLDER, output_filename)

    try:
        encode_message(image_path, message, output_path)
    except ValueError as ve:
        return f"Error: {ve}"

    return render_template('result.html', image=output_path, msg="Encoding successful!")

@app.route('/decode', methods=['POST'])
def decode():
    file = request.files['image']

    if not file:
        return "Please upload an encoded image."

    filename = secure_filename(file.filename)
    unique_filename = f"{int(time.time())}_{filename}"
    image_path = os.path.join(UPLOAD_FOLDER, unique_filename)
    file.save(image_path)

    message = decode_message(image_path)

    return render_template('result.html', message=message, msg="Decoded Message:")

if __name__ == '__main__':
    app.run(debug=True)
