#!/bin/bash

# เข้าไปที่โฟลเดอร์ของ Lab
cd ~/environment/resources/sqs-sns

# ดึง AWS Account ID มาเก็บไว้ในตัวแปร
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Your AWS Account ID is: $ACCOUNT_ID"

# 1. จัดการ Dead-Letter Queue
aws sqs create-queue --queue-name DeadLetterQueue.fifo --attributes file://create-dlq.json
sed -i "s/<FMI_1>/$ACCOUNT_ID/g" dlq-policy.json
aws sqs set-queue-attributes --queue-url "https://sqs.us-east-1.amazonaws.com/$ACCOUNT_ID/DeadLetterQueue.fifo" --attributes file://dlq-policy.json

# 2. จัดการ Main Queue (updated_beans.fifo)
sed -i "s/<FMI_1>/$ACCOUNT_ID/g" create-beans-queue.json
aws sqs create-queue --queue-name updated_beans.fifo --attributes file://create-beans-queue.json
sed -i "s/<FMI_1>/$ACCOUNT_ID/g" beans-queue-policy.json
aws sqs set-queue-attributes --queue-url "https://sqs.us-east-1.amazonaws.com/$ACCOUNT_ID/updated_beans.fifo" --attributes file://beans-queue-policy.json

# 3. จัดการ SNS Topic
TOPIC_ARN=$(aws sns create-topic --name updated_beans_sns.fifo --attributes DisplayName="updated beans sns",ContentBasedDeduplication="true",FifoTopic="true" --query TopicArn --output text)
sed -i "s|<FMI_1>|$TOPIC_ARN|g" beans-topic-policy.json
sed -i "s/<FMI_2>/$ACCOUNT_ID/g" beans-topic-policy.json
aws sns set-topic-attributes --cli-input-json file://beans-topic-policy.json

# 4. Subscribe SQS เข้ากับ SNS
QUEUE_ARN=$(aws sqs get-queue-attributes --queue-url "https://sqs.us-east-1.amazonaws.com/$ACCOUNT_ID/updated_beans.fifo" --attribute-names QueueArn --query Attributes.QueueArn --output text)
aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol sqs --notification-endpoint "$QUEUE_ARN"

# 5. อัปเดตไฟล์ Python เตรียมไว้ให้รันเทส
sed -i "s/<FMI>/$ACCOUNT_ID/g" send_beans_update.py
sed -i "s/<FMI_1>/$ACCOUNT_ID/g" send_beans_update.py

echo "Infrastructure created successfully! 🚀"
echo "Your SQS_ENDPOINT for Elastic Beanstalk is: https://sqs.us-east-1.amazonaws.com/$ACCOUNT_ID/updated_beans.fifo"
