import pandas as pd

df = pd.read_csv('product.csv')


#แบ่งคอลัมน์ 'PRODUCT' ออกเป็นสองคอลัมน์ 'PRODUCT-KEY' และ 'PRODUCT-NAME' โดยใช้ ' ' ช่องว่าง เป็นตัวแบ่ง
#split(' '): ทำการแยกข้อมูลในคอลัมน์ PRODUCT โดยใช้ช่องว่าง (' ') เป็นตัวแบ่ง
#expand=True: จะทำให้ผลลัพธ์ที่ได้จากการแยกข้อมูลถูกขยายออกเป็นหลายคอลัมน์ ซึ่งจะทำให้คุณสามารถใส่ค่าผลลัพธ์ที่แยกแล้วไปในคอลัมน์ใหม่ใน DataFrame
#n=1: กำหนดให้แยกเพียงแค่ครั้งเดียว (แยกข้อมูลออกเป็น 2 ส่วน คือ PRODUCT-KEY และ PRODUCT-NAME) ถ้าข้อมูลในคอลัมน์ PRODUCT มีคำมากกว่า 2 คำ คำที่เหลือจะไปอยู่ใน PRODUCT-NAME
df[['PRODUCT-KEY' , 'PRODUCT-NAME']] = df['PRODUCT'].str.split(' ',expand=True , n=1)

print(df)