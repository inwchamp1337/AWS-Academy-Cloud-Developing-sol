import boto3
import json
import sys

def run_one_shot_lab():
    s3 = boto3.client('s3')
    sts = boto3.client('sts')
    
    try:
        # 1. ดึง Account ID อัตโนมัติ เพื่อความเป๊ะของชื่อ Bucket
        account_id = sts.get_caller_identity()['Account']
        bucket_name = f"s3site-{account_id}"
        my_ip = "203.150.157.117/32" # IP ที่คุณกำหนดมา
        
        print(f"🚀 เริ่มต้นการจัดการสำหรับ Bucket: {bucket_name}")

        # 2. สร้าง Bucket (ถ้ายังไม่มี)
        try:
            s3.create_bucket(Bucket=bucket_name)
            print("✅ ขั้นตอนที่ 1: สร้าง Bucket สำเร็จ")
        except s3.exceptions.BucketAlreadyOwnedByYou:
            print("ℹ️ ขั้นตอนที่ 1: คุณมี Bucket นี้อยู่แล้ว")

        # 3. ปลดล็อก Public Access Block (ต้องทำก่อนใส่ Policy)
        # หมายเหตุ: หากโดน Explicit Deny ที่นี่ แสดงว่า Lab บังคับให้กดหน้าเว็บ
        try:
            s3.put_public_access_block(
                Bucket=bucket_name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False, 'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False, 'RestrictPublicBuckets': False
                }
            )
            print("✅ ขั้นตอนที่ 2: ปลดล็อก Public Access สำเร็จ")
        except Exception as e:
            print(f"⚠️ ขั้นตอนที่ 2 ติดปัญหา: {e}")

        # 4. อัปโหลด index.html (เพื่อให้มีไฟล์รองรับการเข้าชม)
        content = "<html><body><h1>AWS Lab 3.1 Complete by Python</h1></body></html>"
        s3.put_object(Bucket=bucket_name, Key='index.html', Body=content, ContentType='text/html')
        print("✅ ขั้นตอนที่ 3: อัปโหลด index.html สำเร็จ")

        # 5. ใส่ Bucket Policy (ใช้ JSON ที่คุณส่งมา พร้อม IP ของคุณ)
        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{bucket_name}/*",
                    "Condition": {
                        "IpAddress": {
                            "aws:SourceIp": my_ip
                        }
                    }
                }
            ]
        }
        
        s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(policy))
        print("✅ ขั้นตอนที่ 4: ใส่ Bucket Policy (เฉพาะ IP) สำเร็จ")

        # 6. ตั้งค่า Website Hosting
        s3.put_bucket_website(
            Bucket=bucket_name,
            WebsiteConfiguration={'IndexDocument': {'Suffix': 'index.html'}}
        )
        print("✅ ขั้นตอนที่ 5: เปิด Static Website Hosting สำเร็จ")
        
        print("\n✨ ทุกอย่างเรียบร้อย! คุณสามารถกด Submit เพื่อรับคะแนน 15/15 ได้เลยครับ")

    except Exception as e:
        print(f"\n❌ เกิดข้อผิดพลาดร้ายแรง: {e}")
        print("คำแนะนำ: หากติด 'Explicit Deny' แสดงว่า Lab นี้บล็อก API ให้ใช้วิธี 'กดเอง' ในหน้า Console แทนครับ")

if __name__ == "__main__":
    run_one_shot_lab()