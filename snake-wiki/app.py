from flask import Flask, jsonify

app = Flask(__name__)

SNAKE_DATA = {
    "Vine Snake": {"thai": "งูเขียวปากจิ้งจก", "danger": "Mild", "aid": "ล้างแผลปกติ"},
    "Whip Snake": {"thai": "งูแส้หางม้า", "danger": "Mild", "aid": "ล้างแผลปกติ"},
    "Krait": {"thai": "งูทับสมิงคลา", "danger": "High", "aid": "รีบส่งโรงพยาบาล"},
    "Golden Tree": {"thai": "งูเขียวร่อน", "danger": "Mild", "aid": "ทำแผลปกติ"},
    "Russell Viper": {"thai": "งูแมวเซา", "danger": "High", "aid": "อยู่นิ่งๆ ส่งโรงพยาบาล"},
    "Painted Bronzeback": {"thai": "งูสายม่าน", "danger": "None", "aid": "ทำแผลปกติ"},
    "Red-tailed Racer": {"thai": "งูทางมะพร้าว", "danger": "None", "aid": "ทำแผลปกติ"},
    "Sea Krait": {"thai": "งูสมิงทะเล", "danger": "High", "aid": "ส่งโรงพยาบาลด่วน"},
    "Wolf Snake": {"thai": "งูปล้องฉนวน", "danger": "None", "aid": "ทำแผลปกติ"},
    "Monocled Cobra": {"thai": "งูเห่า", "danger": "High", "aid": "ส่งโรงพยาบาลด่วน"},
    "King Cobra": {"thai": "งูจงอาง", "danger": "Critical", "aid": "ส่งโรงพยาบาลด่วนที่สุด"},
    "Protobothrops": {"thai": "งูหัวกะโหลก", "danger": "Moderate", "aid": "พบแพทย์"},
    "Mock Viper": {"thai": "งูคอแดง", "danger": "Moderate", "aid": "สังเกตอาการ"},
    "Python": {"thai": "งูหลาม/เหลือม", "danger": "None", "aid": "ทำแผลปกติ"},
    "Red-necked": {"thai": "งูลายสาบคอแดง", "danger": "High", "aid": "พบแพทย์ทันที"},
    "Bamboo Viper": {"thai": "งูเขียวหางไหม้", "danger": "High", "aid": "ส่งโรงพยาบาล"},
    "Checkered Keelback": {"thai": "งูลายสอ", "danger": "None", "aid": "ล้างแผลปกติ"}
}

@app.route('/info/<name>')
def info(name):
    data = SNAKE_DATA.get(name)
    if not data:
        for key in SNAKE_DATA:
            if key.lower() in name.lower():
                data = SNAKE_DATA[key]
                break
    return jsonify(data if data else {"thai": "Unknown", "danger": "Unknown", "aid": "-"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)