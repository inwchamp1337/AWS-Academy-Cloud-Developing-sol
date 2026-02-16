# AWS Academy Cloud Developing - Lab 5.1

## Description

This Python script automates the completion of AWS Academy Cloud Developing Lab 5.1, which focuses on Amazon DynamoDB operations. It performs the following tasks:

1. Creates the FoodProducts DynamoDB table with a primary key.
2. Adds an "Apple Pie" item using conditional put to ensure it doesn't overwrite existing items.
3. Batch loads product data from a JSON file into the table.
4. Creates a Global Secondary Index (GSI) on the 'special' attribute.
5. Performs a scan operation on the GSI with a filter to demonstrate querying capabilities.

## Prerequisites

- Python 3.x installed on your system.
- AWS CLI configured with appropriate credentials (access key, secret key, and default region set to us-east-1).
- The `boto3` library installed.
- Access to the JSON data file (all_products.json) located at the expected path.

## Installation

1. Ensure Python 3.x is installed. You can download it from [python.org](https://www.python.org/downloads/).

2. Install the required Python package:
   ```
   pip install boto3
   ```

3. Configure AWS credentials using the AWS CLI:
   ```
   aws configure
   ```
   Enter your AWS Access Key ID, Secret Access Key, set default region to `us-east-1`, and output format.

## Preparation

Complete Task 1 first by running the following commands in the Terminal (if not already done):

```bash
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCDEV-2-91558/03-lab-dynamo/code.zip -P /home/ec2-user/environment
unzip -o code.zip
chmod +x ./resources/setup.sh && ./resources/setup.sh
```

Ensure the JSON data file is available. The script looks for it at:
- `/home/ec2-user/environment/resources/website/all_products.json` (AWS Cloud9 environment)
- `../resources/website/all_products.json` (relative path)

If the file is located elsewhere, you may need to modify the `json_path` variable in the script.

## Usage

Run the master script:

```bash
python3 lab51_one_shot_pass.py
```

When the script displays "✨ ทุก Task เสร็จสมบูรณ์!", return to the Lab page and click the blue Submit button.

## Important Notes

- The script is designed for the us-east-1 region. If you need to use a different region, modify the `region` variable in the script.
- Ensure your AWS credentials have permissions for DynamoDB operations (create table, put item, update table, scan).
- The script handles exceptions gracefully, such as when the table or items already exist.
- The GSI creation may take 1-2 minutes to complete.

## Troubleshooting

- If the script fails with authentication errors, verify your AWS credentials and region.
- If the JSON file is not found, check the file paths and ensure the file exists.
- If table creation fails due to resource limits, you may need to increase your DynamoDB capacity or clean up existing resources.
- For any other issues, refer to the AWS DynamoDB documentation or contact your instructor.

## License

This project is for educational purposes as part of AWS Academy Cloud Developing course.