import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import os
import re

# กำหนดเส้นทางโฟลเดอร์ที่เก็บไฟล์
folder_path = 'C:/Users/NT/Downloads/master_files'

# รายการ prefix ของไฟล์ที่ต้องการเลือก
file_prefixes = [
    'MASTER_REVENUE_GL_CODE_NT_', 
    'MASTER_PRODUCT_NT_', 
    'MASTER_ORGANIZATION_NT1.5', 
    'MASTER_EXPENSE_GL_CODE_NT_', 
    'MASTER_ACTIVITY_CODE_'
]

# การตั้งค่าการส่งอีเมล (Gmail)
sender_email = "iklas.co2@gmail.com"
receiver_email = "janprapa.snun@gmail.com"
password = "qpkd bwzw chzg mojy"  # App Password จาก Gmail

# ฟังก์ชันการส่งอีเมล
def send_email(subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # ถ้ามีไฟล์แนบ
    if attachment_path:
        with open(attachment_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
            msg.attach(part)

    # ส่งอีเมล
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent: {subject}")

# ใช้ dictionary เพื่อเก็บไฟล์ที่มีเลขท้ายมากที่สุดสำหรับแต่ละ prefix
latest_files = {}

# ตรวจสอบไฟล์ในโฟลเดอร์
for file_name in sorted(os.listdir(folder_path)):
    if file_name.endswith('.csv'):
        for prefix in file_prefixes:
            if file_name.startswith(prefix):
                # เปรียบเทียบเลือกไฟล์ที่มีเลขท้ายมากที่สุด
                if prefix not in latest_files or file_name > latest_files[prefix]:
                    latest_files[prefix] = file_name

# ตรวจสอบไฟล์และส่งอีเมลเมื่อพบข้อมูลซ้ำ
for prefix, file_name in latest_files.items():
    file_path = os.path.join(folder_path, file_name)  # สร้างพาธไฟล์
    try:
        df = pd.read_csv(file_path)  # อ่านไฟล์ CSV
        print(f"Successfully read: {file_name}")
        
        # ตรวจสอบหาค่าซ้ำใน DataFrame
        df_dup = df[df.duplicated(keep=False)]  # ตรวจหาทุกรายการที่ซ้ำ
        
        # ถ้ามีค่าซ้ำในไฟล์
        if not df_dup.empty:
            # ส่งอีเมลแจ้งเตือนพร้อมแนบไฟล์ต้นฉบับ
            subject = f"Duplicate Data Found in {file_name}"
            body = f"The following rows are duplicated in the file {file_name}:\n\n{df_dup.to_string(index=False)}"
            send_email(subject, body, file_path)  # ส่งอีเมลพร้อมไฟล์แนบต้นฉบับ
        else:
            
            print(f"No duplicates found in {file_name}.")
            
    except Exception as e:
        
        print(f"Error reading {file_name}: {e}")
