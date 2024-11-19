import pandas as pd

# สร้าง DataFrame ที่มีคอลัมน์ชื่อ 'names' และเก็บข้อมูลเป็นรายชื่อ
data = {'names': ['John Smith', 'Jane Doe', 'Mike Johnson']}
df = pd.DataFrame(data)

# ใช้ str.split() เพื่อแยกข้อความในคอลัมน์ 'names' ออกเป็นสองส่วนโดยใช้ช่องว่าง (' ') เป็นตัวแยก
# กำหนด expand=True เพื่อกระจายผลลัพธ์เป็นหลายคอลัมน์
# ผลลัพธ์จะถูกเพิ่มในคอลัมน์ใหม่ชื่อ 'first_name' และ 'last_name'
df[['first_name', 'last_name']] = df['names'].str.split(' ', expand=True)

# แสดง DataFrame ที่อัปเดตแล้ว
print(df)
