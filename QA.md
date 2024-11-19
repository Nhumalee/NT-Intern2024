# QA


**1.กรณีไฟล์ไม่ใช่ UTF-8 ใช้การ encoding 'utf-8'**


>df = pd.read_csv ('randomname.csv',encoding='utf-8')


---
**2.กรณีไฟล์ไม่มี Header ให้ใส่ header=None เพื่อบอกให้ pandas รู้ว่าไม่ต้องใช้แถวแรกเป็นชื่อคอลัมน์**


>df = pd.read_csv ('randomname.csv',encoding='utf-8',header=None).astype(str)


---
**3.อ่านไฟล์และConvert to string**


>df = pd.read_csv ('randomname.csv',encoding='utf-8',header=None).astype(str)


---
__4.วิธีเช็คชนิดข้อมูลในตาราง ใช้ print(df.dtypes)__


>print(df.dtypes)


---


 **Tableau:** 
 
 * เครื่องมือสำหรับการสร้างกราฟและการวิเคราะห์ข้อมูล
 

 **ETL (Extract, Transform, Load):** 
 
 * เป็นการนำข้อมูล(Extract)มาแปลงรูปแบบให้เหมาะสม(Transform)แล้วเก็บ(Load)เข้าไปใน Data


 **Metabase:** 
 
 
 * เครื่องมือสำหรับการวิเคราะห์ข้อมูลและสร้างแดชบอร์ดและเชื่อมต่อกับฐานข้อมูลต่างๆ


**Markdown Format:** 


* รูปแบบการเขียนข้อความที่ง่ายและใช้งานสะดวก ใช้สัญลักษณ์พิเศษ


**Jupyter Python**


* หมายถึงการใช้งาน Python ใน Jupyter Notebook ซึ่งเป็นเครื่องมือที่ใช้เขียนและรันโค้ดแบบอินเทอร์แอคทีฟ โดยเฉพาะในการวิเคราะห์ข้อมูล


---


