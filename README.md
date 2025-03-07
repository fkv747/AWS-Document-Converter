# AWS Document Converter 📄➡️📑

## Overview
This project is a serverless document converter built using AWS services. It allows users to upload `.txt`, `.docx`, and `.xlsx` files and converts them to `.pdf`.

## How It Works
1. The user uploads a file via an API Gateway endpoint.
2. The request triggers an AWS Lambda function.
3. The file is processed and stored in an S3 bucket.
4. The converted PDF is returned to the user.

## AWS Services Used
- **AWS Lambda** for processing files
- **API Gateway** for handling HTTP requests
- **S3** for file storage
- **Fargate** for running the conversion logic

## Screenshots
📷 *VPC Configuration*  
![VPC](docs/screenshots/vpc-setup.png)

📷 *ECS Task Definition*  
![ECS](docs/screenshots/ecs-task.png)

For a full breakdown, check out [ProjectSetup.md](docs/ProjectSetup.md).
