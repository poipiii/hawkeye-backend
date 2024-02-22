import onnxruntime
import cv2
import numpy as np
import os
from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

UPLOAD_FOLDER_BEFORE = 'before'  # Folder where uploaded images are stored initially
UPLOAD_FOLDER_AFTER = 'after'  # Folder where processed images will be stored

app.config['UPLOAD_FOLDER_BEFORE'] = UPLOAD_FOLDER_BEFORE
app.config['UPLOAD_FOLDER_AFTER'] = UPLOAD_FOLDER_AFTER

# Define the path to the "before" and "after" folders
BEFORE_FOLDER_PATH = os.path.join(os.getcwd(), UPLOAD_FOLDER_BEFORE)
AFTER_FOLDER_PATH = os.path.join(os.getcwd(), UPLOAD_FOLDER_AFTER)

# Function to process uploaded image
def process_image(image_path, output_folder):
    # Initialize onnxruntime session
    ort_session = onnxruntime.InferenceSession("run_cugan.onnx", providers=["CPUExecutionProvider"])
    
    # Load the image
    img = cv2.imread(image_path)
    # Resize the image
    img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_CUBIC)
    # Normalize pixel values
    img = img / 255
    # Convert to float32
    img = img.astype(np.float32)
    # Transpose dimensions
    img = img.transpose(2, 0, 1)[None, :, :, :]
    # Send to onnxruntime
    ort_inputs = {"input": img}
    ort_outs = ort_session.run(None, ort_inputs)[0]
    # Back to height x width x 3 array from 0 to 255
    ort_outs = ort_outs[0].transpose(1, 2, 0) * 255
    # Save the processed images into the "after" folder
    cv2.imwrite(output_folder, ort_outs)

# Route to upload image 
@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        # Get image data
        image = request.files['image']
        if image.filename == '':
            return 'No file detected', 400
        # Save image to upload folder
        image_path = os.path.join(app.config['UPLOAD_FOLDER_BEFORE'], image.filename)
        image.save(image_path)
        # Process the uploaded image
        filename = os.path.splitext(image.filename)[0]
        processed_image_path = os.path.join(app.config['UPLOAD_FOLDER_AFTER'], f"{filename}_processed.png")
        process_image(image_path, processed_image_path)
    
        return send_file(processed_image_path)
    return 'Invalid request', 400

# Route to fetch processed images
@app.route('/images')
def get_images():
    images = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER_AFTER']):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            images.append({
                'filename': filename,
                'url': f'/uploads_after/{filename}'
            })
    return jsonify(images)

# Serve processed images
@app.route('/uploads_after/<filename>')
def uploaded_file_after(filename):
    return send_file(os.path.join(app.config['UPLOAD_FOLDER_AFTER'], filename))

# Route to serve index.html
@app.route('/')
def serve_index():
    return send_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
