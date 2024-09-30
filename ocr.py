from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import os

app = Flask(__name__)

# Configure Tesseract executable path (update this path based on your Tesseract installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Route to render the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and OCR processing
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the uploaded image temporarily
    image_path = os.path.join('uploads', file.filename)
    file.save(image_path)

    # Perform OCR using Tesseract on both Hindi and English text
    img = Image.open(image_path)
    extracted_text = pytesseract.image_to_string(img, lang='eng+hin')
    
    # Remove the image after processing
    os.remove(image_path)
    
    # Return the extracted text
    return jsonify({'text': extracted_text})

# Route to handle keyword search
@app.route('/search', methods=['POST'])
def search_keyword():
    data = request.json
    extracted_text = data.get('extracted_text', '')
    keyword = data.get('keyword', '').lower()
    
    # Check if the keyword exists in the extracted text
    if keyword in extracted_text.lower():
        return jsonify({'found': True, 'keyword': keyword})
    else:
        return jsonify({'found': False, 'keyword': keyword})

if __name__ == '__main__':
    # Ensure the upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True, host='0.0.0.0', port=5501)