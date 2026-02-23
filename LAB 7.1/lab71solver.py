import boto3
import json
import zipfile
import io
import time

# --- CONFIGURATION ---
REGION = 'us-east-1'
API_NAME = 'ProductsApi'
STAGE_NAME = 'prod'
BUCKET_KEY_PREFIX = 'lab7-lambda'

# !!! ใส่ให้แล้วครับ !!!
ROLE_ARN = "arn:aws:iam::228029624744:role/LambdaAccessToDynamoDB"

# Clients
lambda_client = boto3.client('lambda', region_name=REGION)
apigw = boto3.client('apigateway', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)
sts = boto3.client('sts')

def get_bucket_name():
    buckets = s3.list_buckets()
    for b in buckets['Buckets']:
        if 'lab-lambda' in b['Name']:
            return b['Name']
    return buckets['Buckets'][0]['Name']

def create_zip_with_specific_filename(code_content, file_name_in_zip):
    zip_output = io.BytesIO()
    with zipfile.ZipFile(zip_output, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.writestr(file_name_in_zip, code_content)
    zip_output.seek(0)
    return zip_output.read()

def main():
    print("--- RUNNING FINAL FIX (With ARN Provided) ---")
    
    bucket_name = get_bucket_name()
    account_id = sts.get_caller_identity()['Account']
    print(f"Target Bucket: {bucket_name}")
    print(f"Using Role: {ROLE_ARN}")

    # ==========================================
    # PART 1: FIX TASK 4 (Create Report Lambda)
    # ==========================================
    print("\n[1/3] Re-creating 'create_report' Lambda...")
    
    # Code ตาม Lab Guide เป๊ะๆ
    code_create_report = """
import json

def lambda_handler(event, context):
    print(event)
    return {
        "msg_str": "Report processing, check your phone shortly"
    }
"""
    # 1. Zip ไฟล์ชื่อ create_report_code.py
    zip_bytes = create_zip_with_specific_filename(code_create_report, 'create_report_code.py')
    s3.put_object(Bucket=bucket_name, Key='create_report_code.zip', Body=zip_bytes)

    # 2. ลบของเก่า (ถ้ามี)
    try:
        lambda_client.delete_function(FunctionName='create_report')
        time.sleep(3)
    except:
        pass

    # 3. สร้างใหม่ (ระบุ Handler: create_report_code.lambda_handler)
    lambda_client.create_function(
        FunctionName='create_report',
        Runtime='python3.8',
        Role=ROLE_ARN,
        Handler='create_report_code.lambda_handler', 
        Code={'S3Bucket': bucket_name, 'S3Key': 'create_report_code.zip'},
        Description='Handles report creation',
        Timeout=15,
        MemorySize=128
    )
    print("  ✅ Lambda 'create_report' created.")

    # ==========================================
    # PART 2: FIX TASK 3C (Mapping Template)
    # ==========================================
    print("\n[2/3] Fixing API Gateway Mapping Template...")
    
    apis = apigw.get_rest_apis()
    api = next((item for item in apis['items'] if item['name'] == API_NAME), None)
    if not api:
        print("❌ API Not Found!")
        return
    api_id = api['id']
    
    resources = apigw.get_resources(restApiId=api_id, limit=500)
    res_on_offer = next((item['id'] for item in resources['items'] if item.get('path') == '/products/on_offer'), None)
    res_report = next((item['id'] for item in resources['items'] if item.get('path') == '/create_report'), None)

    # --- 1. แก้ /products/on_offer ---
    if res_on_offer:
        # ลบ Integration เก่าทิ้งก่อน
        try:
            apigw.delete_integration(restApiId=api_id, resourceId=res_on_offer, httpMethod='GET')
            time.sleep(2)
        except:
            pass

        # สร้างใหม่แบบ AWS Integration (Non-Proxy) + Template
        print("  Applying Mapping Template to /products/on_offer...")
        apigw.put_integration(
            restApiId=api_id,
            resourceId=res_on_offer,
            httpMethod='GET',
            type='AWS', # สำคัญมาก ห้ามเป็น AWS_PROXY
            integrationHttpMethod='POST',
            uri=f"arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:{REGION}:{account_id}:function:get_all_products/invocations",
            requestTemplates={'application/json': '{\n"path": "$context.resourcePath"\n}'}, 
            passthroughBehavior='WHEN_NO_MATCH'
        )
        
        # ใส่ Response CORS
        apigw.put_integration_response(
            restApiId=api_id,
            resourceId=res_on_offer,
            httpMethod='GET',
            statusCode='200',
            responseParameters={'method.response.header.Access-Control-Allow-Origin': "'*'"}
        )
        
        # Add Permission (กันเหนียว)
        try:
            lambda_client.add_permission(
                FunctionName='get_all_products',
                StatementId=f"fix-perm-{int(time.time())}",
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f"arn:aws:execute-api:{REGION}:{account_id}:{api_id}/*/GET/products/on_offer"
            )
        except:
            pass

    # --- 2. แก้ /create_report ---
    if res_report:
        print("  Linking /create_report...")
        try:
            apigw.delete_integration(restApiId=api_id, resourceId=res_report, httpMethod='POST')
            time.sleep(1)
        except:
            pass
            
        apigw.put_integration(
            restApiId=api_id,
            resourceId=res_report,
            httpMethod='POST',
            type='AWS',
            integrationHttpMethod='POST',
            uri=f"arn:aws:apigateway:{REGION}:lambda:path/2015-03-31/functions/arn:aws:lambda:{REGION}:{account_id}:function:create_report/invocations"
        )
        apigw.put_integration_response(
            restApiId=api_id,
            resourceId=res_report,
            httpMethod='POST',
            statusCode='200',
            responseParameters={'method.response.header.Access-Control-Allow-Origin': "'*'"}
        )
        
        try:
            lambda_client.add_permission(
                FunctionName='create_report',
                StatementId=f"fix-report-{int(time.time())}",
                Action='lambda:InvokeFunction',
                Principal='apigateway.amazonaws.com',
                SourceArn=f"arn:aws:execute-api:{REGION}:{account_id}:{api_id}/*/POST/create_report"
            )
        except:
            pass

    # ==========================================
    # PART 3: DEPLOY
    # ==========================================
    print("\n[3/3] Deploying API...")
    apigw.create_deployment(
        restApiId=api_id,
        stageName=STAGE_NAME,
        description=f'Final Fix at {time.time()}'
    )
    print("  ✅ API Deployed.")
    
    print("\n--- เสร็จแล้วครับพี่! กด Submit Grade ได้เลยครับ ---")

if __name__ == '__main__':
    main()