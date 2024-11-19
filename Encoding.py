import pandas as pd

#อ่านชื่อไฟล์ csv
#กรณีไฟล์ไม่ใช่ UTF-8 ใช้การ encoding 'utf-8' 
#กรณีไฟล์ไม่มี Header ให้ใส่ header=None เพื่อบอกให้ pandas รู้ว่าไม่ต้องใช้แถวแรกเป็นชื่อคอลัมน์
#วิธีเช็คชนิดข้อมูลในตาราง ใช้ print(df.dtypes)
df = pd.read_csv ('randomname.csv',encoding='utf-8',header=None)

print(df.dtypes)


