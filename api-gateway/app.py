import os
import requests
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
CORS(app)

# URLs ของแต่ละ Service
S2_URL = "http://localhost:5002/upload"
S3_URL = "http://localhost:5001/predict"
S4_URL = "http://localhost:5003/info"
S5_URL = "http://localhost:5004/log"

def send_log_background(data):
    """ส่ง Log ไปที่ S5 แบบเบื้องหลัง (Background Task) เพื่อไม่ให้หน้าเว็บค้าง"""
    try:
        requests.post(S5_URL, json=data, timeout=2)
    except:
        pass

def call_service(url, files=None, method='POST', params=None):
    """ฟังก์ชันกลางสำหรับส่ง Request ไปยัง Service ต่างๆ"""
    try:
        if method == 'POST':
            resp = requests.post(url, files=files, timeout=10)
        else:
            resp = requests.get(url, timeout=5)
        return resp.json()
    except Exception as e:
        print(f"Service Error at {url}: {e}")
        return None

@app.route('/scan', methods=['POST'])
def scan():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    img_bytes = file.read()
    filename = file.filename
    content_type = file.content_type

    payload_s2 = {'file': (filename, img_bytes, content_type)}
    payload_s3 = {'file': (filename, img_bytes, content_type)}

    with ThreadPoolExecutor(max_workers=2) as executor:
        future_s2 = executor.submit(call_service, S2_URL, files=payload_s2)
        future_s3 = executor.submit(call_service, S3_URL, files=payload_s3)

        storage_res = future_s2.result() or {"url": ""}
        ai_res = future_s3.result() or {"class_name": "Unknown", "confidence": 0.0}

    snake_name = ai_res.get('class_name', 'Unknown')
    wiki_res = call_service(f"{S4_URL}/{snake_name}", method='GET') 
    if not wiki_res:
        wiki_res = {"thai": "ไม่ทราบชื่อ", "danger": "Unknown", "aid": "-"}

    log_payload = {
        "snake_found": snake_name,
        "confidence": ai_res.get('confidence', 0),
        "image_url": storage_res.get("url", "")
    }
    threading.Thread(target=send_log_background, args=(log_payload,)).start()

    return jsonify({
        "status": "success",
        "image_url": storage_res.get("url", ""),
        "prediction": ai_res,
        "info": wiki_res
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)