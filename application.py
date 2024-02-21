from flask import Flask, request, Response, jsonify
from flask_cors import CORS
# import AI model

app = Flask(__name__)



@app.route('/upload', methods=['POST'])
def upload_image():
    if request.method == 'POST':
        # Get image data
        image = request.files['image']
        #image_file = "C:\\Users\\User\\Downloads\\Hawkeye Backend\\0001.png"

        if image.filename == '':
            return 'No file detected', 400
            
        # Send image to AI for processing?

        # Save image just to test
        image.save('C:/Users/User/Downloads/' + image.filename)

    return 'File uploaded successfully', 200



@app.route('/')
def main_page():
    return jsonify({"message": "Test"})
    
if __name__ == '__main__':
  app.run(debug=True)