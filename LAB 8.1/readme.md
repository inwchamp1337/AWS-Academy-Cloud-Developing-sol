# LAB 8.1 Solver

สคริปต์อัตโนมัติสำหรับแก้ไข LAB 8.1 ในหลักสูตร AWS Academy Cloud Developing

## วัตถุประสงค์

สคริปต์นี้ช่วยในการแก้ไข LAB 8.1 โดยอัตโนมัติ ซึ่งเกี่ยวข้องกับการสร้างและจัดการ Docker containers สำหรับ Node.js application และ MySQL database รวมถึงการ push image ไปยัง Amazon ECR และการกำหนดค่า Security Groups

## ข้อกำหนดก่อนใช้งาน

ก่อนรันสคริปต์ กรุณาตรวจสอบว่าคุณมีสิ่งต่อไปนี้:

- Python 3.x ติดตั้งแล้ว
- AWS CLI ติดตั้งและ configure แล้วด้วย credentials ที่ถูกต้อง
- Docker ติดตั้งและรันอยู่
- MySQL client ติดตั้งแล้ว (สำหรับ mysqldump)
- Instance ที่รันสคริปต์ต้องมี IAM role หรือ credentials ที่สามารถเข้าถึง EC2, ECR, และ STS
- Instance ชื่อ 'MysqlServerNode' ต้องทำงานอยู่และสามารถเข้าถึงได้

## การติดตั้ง Dependencies

ติดตั้ง Python packages ที่จำเป็น:

```bash
pip install boto3
```

## วิธีการใช้งาน

1. ดาวน์โหลดหรือ clone repository นี้
2. นำไฟล์ `lab81solver.py` ไปไว้ใน instance ของคุณ
3. รันคำสั่ง:

```bash
python lab81solver.py
```

4. เมื่อสคริปต์ถาม ให้ใส่ Public IP ของ instance ของคุณ
5. รอให้สคริปต์ทำงานเสร็จ (ประมาณ 1-2 นาที)
6. ตรวจสอบผลลัพธ์และกด Submit ใน LAB

## ขั้นตอนที่สคริปต์ทำ

สคริปต์จะทำตามขั้นตอนต่อไปนี้โดยอัตโนมัติ:

1. **Cleanup & Prep**: ลบ containers และไฟล์เก่า ดาวน์โหลดโค้ดใหม่
2. **Find Instance Info**: ค้นหา IP ของ MySQL server instance
3. **Inject Nikki Wolf**: เพิ่มข้อมูล 'Nikki Wolf' เข้า database ภายนอก
4. **Build Node App**: สร้าง Docker image สำหรับ Node.js application
5. **Configure Security Group**: เพิ่ม rule สำหรับ port 3000 ด้วย IP ที่ผู้ใช้ระบุ
6. **MySQL Migration**: สร้าง MySQL container ด้วยข้อมูลที่ migrate จาก server ภายนอก
7. **Internal Linking**: เชื่อมต่อ app กับ MySQL container ภายใน
8. **ECR Push**: Push Docker image ไปยัง Amazon ECR

## คำเตือน

- สคริปต์นี้จะแก้ไข Security Groups และสร้าง resources ใน AWS account ของคุณ
- ตรวจสอบให้แน่ใจว่า credentials และ permissions ถูกต้อง
- หลังรันเสร็จ ให้รอ 1-2 นาทีให้ AWS ตรวจสอบก่อนกด Submit
- หากเกิดข้อผิดพลาด ให้ตรวจสอบ logs และแก้ไขตามความเหมาะสม

## ผลลัพธ์ที่คาดหวัง

หลังรันสคริปต์สำเร็จ คุณจะได้:

- Node.js application รันอยู่ที่ port 3000
- MySQL database ใน container พร้อมข้อมูล
- Docker image ที่ push ไปยัง ECR แล้ว
- Security Group ที่อนุญาตการเข้าถึงจาก IP ที่ระบุ

## การแก้ปัญหา

หากสคริปต์ไม่ทำงาน:

- ตรวจสอบว่า AWS credentials ถูกต้อง
- ตรวจสอบว่า Docker daemon รันอยู่
- ตรวจสอบว่า instance 'MysqlServerNode' เข้าถึงได้
- ตรวจสอบ logs จาก output ของสคริปต์

---

**หมายเหตุ**: สคริปต์นี้สร้างขึ้นเพื่อการศึกษาและการฝึกปฏิบัติใน AWS Academy เท่านั้น