from flask import Flask, render_template, request, jsonify
import openrouteservice
from geopy.distance import geodesic
import json

# สร้างแอปพลิเคชัน Flask ซึ่งเป็นเว็บเฟรมเวิร์กที่ใช้สำหรับสร้าง API และการจัดการหน้าเว็บ
app = Flask(__name__)

# เปิดการเชื่อมต่อกับ OpenRouteService API โดยต้องใช้ API Key สำหรับการเข้าถึงบริการ
# OpenRouteService ช่วยในการคำนวณเส้นทางและระยะทางระหว่างตำแหน่งสองจุด
client = openrouteservice.Client(key='5b3ce3597851110001cf6248fd8d5ee041fd4656ae87939e0df0c20f')

# โหลดข้อมูลศูนย์บริการ (service centers) จากไฟล์ JSON ที่กำหนด
try:
    # เปิดไฟล์ JSON ที่เก็บข้อมูลศูนย์บริการ (เช่น ชื่อ, พิกัด, เบอร์โทร)
    with open(r'C:\Users\NT\Desktop\Intern\Python\Python-Basic\nt_service_center\nt_service_center.json', 'r', encoding='utf-8') as file:
        service_centers = json.load(file)  # อ่านข้อมูลไฟล์ JSON และแปลงเป็นรูปแบบ Python dictionary
except FileNotFoundError:
    # กรณีไม่พบไฟล์ ให้แสดงข้อความแจ้งเตือน และตั้งค่าข้อมูลศูนย์บริการเป็นลิสต์ว่าง
    print("Error: ข้อมูลไฟล์ศูนย์บริการไม่พบ")
    service_centers = []

# สร้าง route สำหรับหน้าเว็บหลัก
@app.route('/')
def index():
    # Render หน้า HTML ชื่อ index2.html ซึ่งเป็นไฟล์เทมเพลตที่ออกแบบหน้าตาของเว็บ
    return render_template('index2.html')

# สร้าง route สำหรับรับข้อมูลตำแหน่งของผู้ใช้และค้นหาศูนย์บริการที่ใกล้ที่สุด
@app.route('/get_location', methods=['POST'])
def get_location():
    # ดึงข้อมูลตำแหน่งจาก request ที่ส่งมาจากฝั่งไคลเอนต์ในรูปแบบ JSON
    data = request.get_json()

    # ตรวจสอบว่าข้อมูลที่ได้รับมี 'latitude' และ 'longitude' หรือไม่
    if not data or 'latitude' not in data or 'longitude' not in data:
        # หากข้อมูลไม่ครบถ้วน ให้ส่งข้อผิดพลาดกลับไปยังไคลเอนต์
        return jsonify({"error": "Invalid data"}), 400

    # อ่านค่า latitude และ longitude จากข้อมูลที่ได้รับ
    user_lat = data['latitude']  # ละติจูดตำแหน่งของผู้ใช้
    user_lon = data['longitude']  # ลองจิจูดตำแหน่งของผู้ใช้

    # ตัวแปรสำหรับเก็บศูนย์บริการที่ใกล้ที่สุดและระยะทางที่สั้นที่สุด
    closest_center = None  # ค่าเริ่มต้นเป็น None
    min_distance = float('inf')  # ค่าเริ่มต้นของระยะทางเป็นค่ามากที่สุด (Infinity)

    # ค้นหาศูนย์บริการที่ใกล้ที่สุด
    for center in service_centers:
        # ตรวจสอบว่าศูนย์บริการมีข้อมูลพิกัด (latitude และ longitude) หรือไม่
        if 'lat' not in center or 'lng' not in center:
            continue  # หากไม่มีข้อมูลพิกัด ให้ข้ามไปยังศูนย์บริการถัดไป

        # พิกัดของศูนย์บริการ
        center_coords = (center['lat'], center['lng'])
        # พิกัดของผู้ใช้
        user_coords = (user_lat, user_lon)

        # คำนวณระยะทางระหว่างผู้ใช้และศูนย์บริการโดยใช้ฟังก์ชัน geodesic จาก geopy
        distance = geodesic(user_coords, center_coords).km

        # เปรียบเทียบระยะทางปัจจุบันกับระยะทางที่เก็บไว้ว่าศูนย์บริการนี้ใกล้กว่าหรือไม่
        if distance < min_distance:
            min_distance = distance  # อัปเดตระยะทางที่สั้นที่สุด
            closest_center = center  # บันทึกข้อมูลศูนย์บริการที่ใกล้ที่สุด

    # หากไม่พบศูนย์บริการที่ใกล้ที่สุด (เช่น ข้อมูลในไฟล์ JSON อาจว่าง)
    if closest_center is None:
        # ส่งข้อความแจ้งเตือนกลับไปยังไคลเอนต์
        return jsonify({"error": "No service centers found"}), 404

    # จัดรูปแบบข้อมูลศูนย์บริการที่ใกล้ที่สุดในรูปแบบ dictionary
    service_info = {
        "service_code": closest_center.get('n', 'ไม่พบข้อมูล'),  # รหัสศูนย์บริการ
        "name": closest_center.get('nm', 'ไม่พบข้อมูล'),  # ชื่อศูนย์บริการ
        "address": f"{closest_center.get('add', 'ไม่พบข้อมูล')} {closest_center.get('tb', 'ไม่พบข้อมูล')} {closest_center.get('pv', 'ไม่พบข้อมูล')} {closest_center.get('pc', 'ไม่พบข้อมูล')}",  # ที่อยู่
        "bus_stops": closest_center.get('bs', 'ไม่พบข้อมูล'),  # ข้อมูลป้ายรถเมล์ใกล้เคียง
        "opening_time": closest_center.get('tf', 'ไม่พบข้อมูล'),  # เวลาเปิดทำการ
        "phone": closest_center.get('tp', 'ไม่พบข้อมูล')  # เบอร์โทรศัพท์
    }

    # ตรวจสอบว่าศูนย์บริการที่เลือกมีข้อมูลพิกัด (latitude และ longitude) ครบถ้วน
    if 'lat' not in closest_center or 'lng' not in closest_center:
        return jsonify({"error": "Invalid service center coordinates"}), 400

    # สร้างพิกัดสำหรับคำนวณเส้นทาง
    user_coords = [user_lon, user_lat]  # พิกัดของผู้ใช้ในรูปแบบ [longitude, latitude]
    center_coords = [closest_center['lng'], closest_center['lat']]  # พิกัดศูนย์บริการในรูปแบบ [longitude, latitude]

    try:
        # ขอเส้นทางระหว่างผู้ใช้และศูนย์บริการจาก OpenRouteService API
        routes = client.directions(
            coordinates=[user_coords, center_coords],  # กำหนดจุดเริ่มต้นและจุดหมาย
            profile='driving-car',  # ใช้โปรไฟล์สำหรับการเดินทางด้วยรถยนต์
            format='geojson',  # กำหนดรูปแบบข้อมูลที่ต้องการ
            instructions=False  # ปิดการแสดงคำแนะนำสำหรับเส้นทาง
        )
    except openrouteservice.exceptions.ApiError as e:
        # หากเกิดข้อผิดพลาดในการเรียกใช้ API ให้ส่งข้อความแจ้งกลับไป
        return jsonify({"error": "Error with OpenRouteService API: " + str(e)}), 500
    except Exception as e:
        # หากเกิดข้อผิดพลาดอื่น ๆ ให้ส่งข้อความแจ้งกลับไป
        return jsonify({"error": "Unexpected error: " + str(e)}), 500

    # ส่งข้อมูลกลับไปยังไคลเอนต์ในรูปแบบ JSON
    return jsonify({
        'closest_center': closest_center,  # ข้อมูลศูนย์บริการที่ใกล้ที่สุด
        'distance': min_distance,  # ระยะทางจากผู้ใช้ถึงศูนย์บริการ
        'route': routes['features'][0]['geometry']['coordinates'],  # พิกัดของเส้นทาง
        'service_info': service_info  # ข้อมูลเพิ่มเติมของศูนย์บริการ
    })

# ฟังก์ชันสำหรับรันแอปพลิเคชัน
if __name__ == '__main__':
    # เปิดโหมด debug เพื่อช่วยตรวจสอบข้อผิดพลาดขณะพัฒนา
    app.run(debug=True)
