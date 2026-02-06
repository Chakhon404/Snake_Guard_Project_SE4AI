import os
import uuid
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    filename = f"{uuid.uuid4()}_{file.filename}"
    file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    return jsonify({"url": f"http://localhost:5002/uploads/{filename}"})

@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)