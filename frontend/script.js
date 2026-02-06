async function scanSnake() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    
    if (!file) { alert("กรุณาเลือกไฟล์รูปภาพ!"); return; }

    // Reset UI
    document.getElementById('result').style.display = 'none';
    document.getElementById('loader').style.display = 'block';
    
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('http://localhost:5000/scan', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        document.getElementById('loader').style.display = 'none';

        // --- แก้ไข: เช็คก่อนว่ามี prediction ส่งมาไหม ---
        if (data.status === 'success' && data.prediction) {
            // Show Image
            const img = document.getElementById('preview');
            img.src = data.image_url;
            img.style.display = 'block';

            // Show Text
            document.getElementById('result').style.display = 'block';
            // ใส่การเช็คป้องกัน undefined อีกชั้น
            const className = data.prediction.class_name || "Unknown"; 
            const conf = data.prediction.confidence || 0;
            
            document.getElementById('snakeName').innerText = className;
            document.getElementById('confidence').innerText = (conf * 100).toFixed(1) + "%";
            
            // Show Wiki Info
            if (data.info) {
                document.getElementById('thaiName').innerText = data.info.thai || "-";
                document.getElementById('danger').innerText = data.info.danger || "-";
                document.getElementById('aid').innerText = data.info.aid || "-";
            }
        } else {
            // ถ้า Server ตอบกลับมาแต่เป็น Error
            console.error("Server Error Response:", data);
            alert("เกิดข้อผิดพลาดจาก Server: " + (data.error || JSON.stringify(data)));
        }

    } catch (error) {
        console.error("Network/JS Error:", error);
        alert("เชื่อมต่อไม่ได้! (ตรวจสอบว่าหน้าต่าง Gateway และ AI เปิดอยู่หรือไม่)");
        document.getElementById('loader').style.display = 'none';
    }
}