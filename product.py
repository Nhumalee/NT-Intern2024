import pandas as pd 
import numpy as np

# อ่านไฟล์ CSV ชื่อ "product.csv" และเก็บไว้ใน DataFrame
df = pd.read_csv("product.csv", encoding='utf-8')

# สุ่มข้อมูลจากคอลัมน์ 'PRODUCT_KEY' 200 แถว พร้อมล็อกค่าให้เหมือนเดิมทุกครั้ง
random_product1 = df[['PRODUCT_KEY']].sample(n=200, random_state=100).reset_index(drop=True)
np.random.seed(100)  # กำหนด seed สำหรับการสุ่มใน numpy
# เพิ่มคอลัมน์ A, B และ C พร้อมสุ่มค่าให้แต่ละคอลัมน์
random_product1['A'] = np.random.randint(1, 501, size=len(random_product1))
random_product1['B'] = np.random.choice(['ก', 'ข', 'ค', 'ง', 'จ', 'ฉ', 'ช', 'ซ', 'ญ', 'ฎ'], size=len(random_product1))
random_product1['C'] = np.random.choice(['๐', '๑', '๒', '๓', '๔', '๕', '๖', '๗', '๘', '๙'], size=len(random_product1))

# สุ่มข้อมูลจากคอลัมน์ 'PRODUCT_KEY' 100 แถว พร้อมล็อกค่าให้เหมือนเดิมทุกครั้ง
random_product2 = df[['PRODUCT_KEY']].sample(n=100, random_state=70).reset_index(drop=True)
np.random.seed(70)  # กำหนด seed สำหรับการสุ่มใน numpy
# เพิ่มคอลัมน์ D และ E พร้อมสุ่มค่าให้แต่ละคอลัมน์
random_product2['D'] = np.random.choice(['แดง', 'เขียว', 'น้ำเงิน', 'เหลือง', 'ส้ม', 'ม่วง', 'ชมพู', 'ขาว', 'ดำ'], size=len(random_product2))
random_product2['E'] = np.random.choice(['กรุงเทพฯ', 'เชียงใหม่', 'ภูเก็ต', 'นครราชสีมา', 'ขอนแก่น', 'สุราษฎร์ธานี', 'เชียงราย'], size=len(random_product2))

# สุ่มข้อมูลจากคอลัมน์ 'PRODUCT_KEY' 50 แถว พร้อมล็อกค่าให้เหมือนเดิมทุกครั้ง
random_product3 = df[['PRODUCT_KEY']].sample(n=50, random_state=20).reset_index(drop=True)
np.random.seed(20)  # กำหนด seed สำหรับการสุ่มใน numpy
# เพิ่มคอลัมน์ F, G และ H พร้อมสุ่มค่าให้แต่ละคอลัมน์
random_product3['F'] = np.random.choice(['ข้าวผัด', 'ผัดไทย', 'ส้มตำ', 'ต้มยำ', 'แกงเขียวหวาน', 'ขนมจีนน้ำยา', 'ปูผัดผงกะหรี่'], size=len(random_product3))
random_product3['G'] = np.random.choice(['หมอ', 'ครู', 'นักวิทยาศาสตร์', 'นักบัญชี', 'นักออกแบบ', 'วิศวกร', 'นักพัฒนา'], size=len(random_product3))
random_product3['H'] = np.random.choice(['แมว', 'สุนัข', 'กระต่าย', 'ช้าง', 'ม้า', 'ปลา', 'นก', 'เสือ', 'มังกร'], size=len(random_product3))

# รวมทั้งสาม DataFrame โดยใช้ pd.concat() และตั้งค่า axis=0 เพื่อรวมในแนวตั้ง (ตามแถว)
#merged_df = pd.concat([random_product1, random_product2, random_product3], axis=0).reset_index(drop=True)


merged_df = pd.merge(random_product1, random_product2, on='PRODUCT_KEY', how='outer')
merged_df = pd.merge(merged_df, random_product3, on='PRODUCT_KEY', how='outer')

# แสดงผลลัพธ์ DataFrame ที่รวมข้อมูล
#print(random_product3)
merged_df.to_csv('product_py.csv', index=False, encoding='utf-8-sig')

