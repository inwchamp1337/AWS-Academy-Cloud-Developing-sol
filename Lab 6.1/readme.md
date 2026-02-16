# AWS Academy Cloud Developing - Lab 6.1: Creating a REST API with Amazon API Gateway

## Overview

This lab focuses on migrating the Café website from using hardcoded JSON files stored in S3 to a dynamic, scalable architecture using Amazon API Gateway. This serves as the second major milestone in building a serverless dynamic website.

**Important Note:** This lab cannot be automated using Python scripts. You must complete all steps manually through the AWS Management Console and VS Code editor. Do not attempt to use automated scripts as the lab requires hands-on interaction with the AWS console to understand the concepts.

## Lab Objectives

1. Configure the development environment
2. Create a REST API using Amazon API Gateway
3. Set up mock integrations for testing
4. Deploy the API and integrate it with the website
5. Verify the implementation

## Prerequisites

- Access to AWS Academy Cloud Developing environment
- VS Code IDE configured
- Basic understanding of REST APIs and HTTP methods

## Step-by-Step Instructions

### 1. Development Environment Preparation

#### Resource Acquisition
Download and extract the lab's core assets:
```bash
wget https://aws-tc-largeobjects.s3.us-west-2.amazonaws.com/CUR-TF-200-ACCDEV-2-91558/04-lab-api/code.zip -P /home/ec2-user/environment
unzip -o code.zip
```

#### Dependency Management
Execute the setup script to install required dependencies:
```bash
chmod +x ./resources/setup.sh && ./resources/setup.sh
```

#### Security Configuration
Update S3 bucket policies with your public IPv4 address to ensure secure access to hosted assets.

### 2. API Architecture Construction

Manually create the ProductsApi in the AWS API Gateway console with the following structure:

#### API Resources and Methods:
- **/products** (GET) - Retrieves the full list of menu items
- **/products/on_offer** (GET) - Filters and retrieves items currently on promotion
- **/create_report** (POST) - Supports authenticated requests for inventory reporting

### 3. Mock Integration Setup

For each endpoint, configure Mock Integrations:

#### Integration Request:
- Set up to return 200 OK status for all valid calls

#### Integration Response:
- Use responseTemplates to return hardcoded JSON data
- Map JSON structure to match DynamoDB attributes:
  - Use "S" for strings
  - Use "N" for numbers

Example mock response for /products:
```json
{
  "Items": [
    {
      "product_name": {"S": "Sample Product"},
      "price_in_cents": {"N": "1000"},
      "description": {"S": "Sample description"}
    }
  ]
}
```

### 4. Deployment and Website Integration

#### Deploy the API:
- Create a new deployment stage named `prod` (case-sensitive)
- Capture the Invoke URL (e.g., `https://[api-id].execute-api.us-east-1.amazonaws.com/prod`)

#### Update Configuration:
- Edit `config.js` and update the API endpoint URL
- Ensure no trailing slash in the URL to prevent 403/401 errors

#### Synchronize with S3:
- Run the update script to upload changes:
```bash
python3 update_config.py
```

### 5. Verification and Testing

Verify successful implementation through:

#### Browser Developer Console:
- Confirm shift from "Using hardcoded data" to "Using API Gateway"

#### UI Behavior:
- "View All" should display exactly 3 products (mock data) instead of original 6

#### HTTP Status Codes:
- Successful GET requests return 200 status
- Unauthorized POST requests to /create_report should fail appropriately

## Important Notes

- **Manual Process Required:** Unlike previous labs, this lab requires manual configuration through the AWS Console. Python automation is not applicable here as the lab is designed to teach API Gateway concepts through hands-on experience.
- Ensure all API methods are properly configured with correct request/response mappings
- Test each endpoint individually before proceeding to deployment
- The mock data should exactly match the expected DynamoDB format for future Lambda integration

## Troubleshooting

- If you receive 403/401 errors, check the Invoke URL for trailing slashes
- Ensure the deployment stage is correctly named as `prod`
- Verify that mock integrations are properly configured for each method
- Check browser console for detailed error messages

## Next Steps

After completing this lab, you will be prepared for Lab 6.2, which involves integrating Lambda functions with the API Gateway to create a fully dynamic serverless backend.

## License

This project is for educational purposes as part of AWS Academy Cloud Developing course.