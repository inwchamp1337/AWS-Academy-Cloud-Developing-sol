# AWS Academy Cloud Developing - Lab 3.1

## Description

This Python script automates the setup of an Amazon S3 bucket for hosting a static website as part of AWS Academy Cloud Developing Lab 3.1. It performs the following tasks:

1. Creates an S3 bucket with a name based on your AWS account ID.
2. Disables public access block settings.
3. Uploads a simple index.html file.
4. Applies a bucket policy that allows public read access only from a specific IP address.
5. Enables static website hosting on the bucket.

## Prerequisites

- Python 3.x installed on your system.
- AWS CLI configured with appropriate credentials (access key, secret key, and default region).
- The `boto3` library installed.
- Your public IP address (the script uses a hardcoded IP; update it if necessary).

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
   Enter your AWS Access Key ID, Secret Access Key, default region, and output format.

## Usage

1. Clone or download this repository to your local machine.

2. Navigate to the `Lab 3.1` directory:
   ```
   cd "Lab 3.1"
   ```

3. (Optional) Update the IP address in `ultimate_run.py` if your public IP has changed. The current IP is set to `203.150.157.117/32`. You can find your current public IP by visiting [whatismyipaddress.com](https://whatismyipaddress.com/).

4. Run the script:
   ```
   python ultimate_run.py
   ```

5. The script will output progress messages. If successful, it will indicate that the setup is complete.

6. After running the script, you can submit your lab work for grading.

## Important Notes

- The bucket policy restricts access to the specified IP address for security reasons.
- If you encounter an "Explicit Deny" error, it may be due to AWS Academy's restrictions on API calls for this lab. In such cases, you may need to perform the steps manually through the AWS Management Console.
- Ensure your AWS credentials have the necessary permissions to create S3 buckets, set policies, and configure website hosting.

## Troubleshooting

- If the script fails with authentication errors, double-check your AWS credentials.
- If bucket creation fails due to name conflicts, the script will notify you if the bucket already exists.
- For any other issues, refer to the AWS documentation or contact your instructor.

## License

This project is for educational purposes as part of AWS Academy Cloud Developing course.