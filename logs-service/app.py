from flask import Flask, request, jsonify
app = Flask(__name__)
logs = []
@app.route('/log', methods=['POST'])
def log():
    logs.append(request.json)
    print(f"Log: {request.json}")
    return jsonify({"status": "saved"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
