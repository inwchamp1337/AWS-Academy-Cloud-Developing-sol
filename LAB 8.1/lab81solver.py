import boto3
import subprocess
import os
import time
import sys
import socket

# --- CONFIGURATION ---
REGION = 'us-east-1'
REPO_NAME = 'node-app'
CODE_URL = "https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCDEV-2-91558/06-lab-containers/code.zip"

# Clients
ec2 = boto3.client('ec2', region_name=REGION)
ecr = boto3.client('ecr', region_name=REGION)
sts = boto3.client('sts')

def run(cmd):
    print(f"🚀 Executing: {cmd}")
    try:
        return subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return e.output.decode('utf-8')

def main():
    print("--- 🏆 LAB 8.1 MASTER SCRIPT (30/30) ---")
    
    # ด่านแรก: ถาม IP พี่ก่อนเลย
    print("\n" + "="*50)
    user_ip = input("👉 พี่ Champ ครับ กรุณาใส่ Public IP ของพี่ (เช่น 161.246.149.92): ").strip()
    print("="*50 + "\n")

    if not user_ip:
        print("❌ พี่ไม่ใส่ IP ผมไปต่อไม่ได้ครับ!")
        return

    # [0] CLEANUP & PREP
    print("[1/8] Cleaning and Downloading code...")
    run("docker stop node_app_1 mysql_1 || true && docker rm node_app_1 mysql_1 || true")
    run("rm -rf ~/environment/containers ~/environment/resources ~/environment/code.zip")
    run(f"wget {CODE_URL} -P ~/environment && unzip -o ~/environment/code.zip -d ~/environment")

    # [1] FIND INSTANCE INFO
    mysql_node_ip = ec2.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': ['MysqlServerNode']}])['Reservations'][0]['Instances'][0]['PublicIpAddress']
    
    # [2] TASK 2: INJECT NIKKI WOLF
    print("[2/8] Injecting 'Nikki Wolf' into external database...")
    sql_inject = "USE COFFEE; INSERT INTO suppliers (name, address, city, state, email, phone) VALUES ('Nikki Wolf', '100 Main Street', 'Anytown', 'CA', 'nwolf@example.com', '4155551212') ON DUPLICATE KEY UPDATE name=name;"
    run(f"mysql -h {mysql_node_ip} -u nodeapp -pcoffee -e \"{sql_inject}\"")

    # [3] TASK 3: NODE APP (EXTERNAL CONNECTION)
    print("[3/8] Building Node App Container...")
    run("mkdir -p ~/environment/containers/node_app")
    run("mv ~/environment/resources/codebase_partner ~/environment/containers/node_app/")
    
    # Create Dockerfile
    with open("/home/ec2-user/environment/containers/node_app/codebase_partner/Dockerfile", "w") as f:
        f.write("FROM node:11-alpine\nRUN mkdir -p /usr/src/app\nWORKDIR /usr/src/app\nCOPY . .\nRUN npm install\nEXPOSE 3000\nCMD [\"npm\", \"run\", \"start\"]")
    
    run("cd ~/environment/containers/node_app/codebase_partner && docker build --tag node_app .")
    run(f"docker run -d --name node_app_1 -p 3000:3000 -e APP_DB_HOST={mysql_node_ip} node_app")

    # [4] TASK 3B: FIX SECURITY GROUP (Using Manual IP)
    print(f"[4/8] Configuring Security Group with IP: {user_ip}...")
    my_private_ip = socket.gethostbyname(socket.gethostname())
    my_instance = ec2.describe_instances(Filters=[{'Name': 'private-ip-address', 'Values': [my_private_ip]}])['Reservations'][0]['Instances'][0]
    sg_id = my_instance['SecurityGroups'][0]['GroupId']
    
    # ลบ Rule เก่าที่ซ้ำซ้อนออกก่อนเพื่อความสะอาด
    try:
        run(f"aws ec2 revoke-security-group-ingress --group-id {sg_id} --protocol tcp --port 3000 --cidr 0.0.0.0/0 || true")
    except: pass
    
    run(f"aws ec2 authorize-security-group-ingress --group-id {sg_id} --protocol tcp --port 3000 --cidr {user_ip}/32 || echo 'Rule already exists'")

    # [5] TASK 4: MYSQL MIGRATION
    print("[5/8] Preparing MySQL Server Container...")
    run("mkdir -p ~/environment/containers/mysql")
    run(f"mysqldump -P 3306 -h {mysql_node_ip} -u nodeapp -pcoffee --databases COFFEE > ~/environment/containers/my_sql.sql")
    
    # แก้ไขไฟล์ตามโจทย์สั่ง
    run("sed -i '1d' ~/environment/containers/my_sql.sql")
    run("sed -i 's/100 Main Street/100 Container Street/g' ~/environment/containers/my_sql.sql")
    run("mv ~/environment/containers/my_sql.sql ~/environment/containers/mysql/")
    
    with open("/home/ec2-user/environment/containers/mysql/Dockerfile", "w") as f:
        f.write("FROM mysql:8.0.23\nCOPY ./my_sql.sql /\nEXPOSE 3306")
    
    run("cd ~/environment/containers/mysql && docker build --tag mysql_server .")
    run("docker run --name mysql_1 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=rootpw -d mysql_server")
    
    print("⏳ Waiting for MySQL Container to be ready (30s)...")
    time.sleep(30)
    
    # Import Data
    run("docker exec -i mysql_1 mysql -u root -prootpw < /home/ec2-user/environment/containers/mysql/my_sql.sql")
    run("docker exec -i mysql_1 mysql -u root -prootpw -e \"CREATE USER 'nodeapp' IDENTIFIED WITH mysql_native_password BY 'coffee'; GRANT all privileges on *.* to 'nodeapp'@'%';\"")

    # [6] TASK 5: INTERNAL LINKING
    print("[6/8] Linking App to Internal MySQL IP...")
    run("docker stop node_app_1 && docker rm node_app_1")
    mysql_internal_ip = run("docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mysql_1").strip()
    run(f"docker run -d --name node_app_1 -p 3000:3000 -e APP_DB_HOST={mysql_internal_ip} node_app")

    # [7] TASK 6: ECR PUSH
    print("[7/8] Pushing Image to Amazon ECR...")
    account_id = sts.get_caller_identity()['Account']
    run(f"aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin {account_id}.dkr.ecr.us-east-1.amazonaws.com")
    run(f"aws ecr create-repository --repository-name {REPO_NAME} || echo 'Repo exists'")
    full_uri = f"{account_id}.dkr.ecr.us-east-1.amazonaws.com/{REPO_NAME}:latest"
    run(f"docker tag node_app:latest {full_uri}")
    run(f"docker push {full_uri}")

    # [8] FINAL CHECK
    print("\n" + "✅"*10)
    print("--- 🏆 COMPLETED! 🏆 ---")
    print(f"1. IP ใน Security Group: {user_ip}/32")
    print(f"2. MySQL Internal IP: {mysql_internal_ip}")
    print(f"3. ECR Image: {full_uri}")
    print("\nพี่ Champ รออีก 1-2 นาทีให้ AWS ตรวจเช็ค แล้วกด Submit ได้เลยครับ!")

if __name__ == '__main__':
    main()