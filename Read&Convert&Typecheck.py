import pandas as pd  # นำเข้าไลบรารี pandas

# ตัวอย่าง DataFrame ที่ประกอบด้วยข้อมูลสามคอลัมน์
data = {
    'ID': [1, 2, 3],  # คอลัมน์ ID ที่มีค่าตัวเลข
    'Name': ['John', 'Alice', 'Bob'],  # คอลัมน์ Name ที่มีค่าข้อความ
    'Age': [25, 30, 22]  # คอลัมน์ Age ที่มีค่าตัวเลข
}

df = pd.DataFrame(data)  # สร้าง DataFrame จาก dictionary ที่มีข้อมูลข้างต้น
print(df)  # แสดง DataFrame ที่สร้างขึ้น
print(df.dtypes)  # แสดงประเภทข้อมูล (dtypes) ของแต่ละคอลัมน์ใน DataFrame



# การแปลงข้อมูลในคอลัมน์ 'Age' เป็นประเภท string (str)
df['Age'] = df['Age'].astype(str)  # ใช้ astype() เพื่อแปลงคอลัมน์ 'Age' เป็น string
print(df)  # แสดง DataFrame หลังจากการแปลงข้อมูล
print(df.dtypes)  # แสดงประเภทข้อมูล (dtypes) ของแต่ละคอลัมน์ใน DataFrame หลังจากการแปลง
