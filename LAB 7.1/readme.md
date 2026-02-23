# LAB 7.1 Automation Script

This script automates the completion of LAB 7.1 in the AWS Academy Cloud Developing course, focusing on AWS Lambda, API Gateway, and DynamoDB integration.

## 🛠️ Pre-requisites (Before running the script)

Before executing the automation script, you must complete these steps to prepare the AWS environment:

### Initialize Lab Environment:
Run the setup script provided by the lab to create the S3 bucket and DynamoDB table.

```bash
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCDEV-2-91558/05-lab-lambda/code.zip -P /home/ec2-user/environment
unzip code.zip
chmod +x resources/setup.sh && ./resources/setup.sh
# Enter your Public IP address when prompted.
```

### Obtain the IAM Role ARN:
The script requires a specific IAM Role to grant Lambda permission to read from DynamoDB.

- Go to the IAM Console > Roles.
- Search for `LambdaAccessToDynamoDB`.
- Copy the Role ARN (e.g., `arn:aws:iam::123456789012:role/LambdaAccessToDynamoDB`).

### Verify API Gateway:
Ensure the `ProductsApi` was created by the initial setup script.

## 🚀 Execution Guide

### Clone the automation script:
Navigate to your Python directory:

```bash
cd ~/environment/python_3
```

### Configure the script:
Open `lab71solver.py` and paste your copied Role ARN into the configuration variable:

```python
ROLE_ARN = "PASTE_YOUR_COPIED_ARN_HERE"
```

### Run the script:

```bash
python3 lab71solver.py
```

## ✅ What this script automates

- **Task 2 & 4**: Creates two Lambda functions (`get_all_products`, `create_report`) with correct Python logic.
- **Task 3 & 5**: Links API Gateway resources to the Lambda functions.
- **Task 3C**: Configures the crucial Mapping Template for `/products/on_offer` to handle path filtering.
- **CORS Management**: Enables Cross-Origin Resource Sharing for all GET methods.
- **Auto-Deployment**: Deploys the API to the `prod` stage.
- **Frontend Sync**: Updates `config.js` and uploads it to S3, making the website live.

## 📂 Project Structure

```
.
├── lab71solver.py       # Main automation script
├── README.md            # Lab documentation
└── resources/           # Original lab resources
```

Author: [Your Name / Champ]  
Lab Version: 1.0.10

## Checklist: Things to check for 100% completion

If you're writing a summary on GitHub, I recommend including this list to show what results you get:

- [x] **[TASK 2]** `get_all_products` function created
- [x] **[TASK 3]** `/products` GET linked to Lambda
- [x] **[TASK 3C]** Mapping template configured (the key point)
- [x] **[TASK 4]** `create_report` function created
- [x] **[TASK 6]** Website displaying live DynamoDB data