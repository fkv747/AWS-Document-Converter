import boto3
import json

# Initialize S3 client
s3 = boto3.client("s3")
BUCKET_NAME = "convert-to-pdf-storage"

def lambda_handler(event, context):
    try:
        # Parse HTTP API request body safely
        body = json.loads(event.get("body", "{}"))

        file_name = body.get("file_name")
        file_type = body.get("file_type", "application/octet-stream")

        if not file_name:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing file_name parameter"})
            }

        # Generate pre-signed URL for uploading the file
        upload_url = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": f"uploads/{file_name}",
                "ContentType": file_type
            },
            ExpiresIn=300  # Upload URL expires in 5 minutes
        )

        # Generate pre-signed URL for downloading the converted PDF
        pdf_key = f"converted/{file_name}.pdf"
        download_url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": BUCKET_NAME, "Key": pdf_key},
            ExpiresIn=3600  # Download link expires in 1 hour
        )

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({
                "upload_url": upload_url,
                "pdf_url": download_url  # Secure pre-signed URL for downloading
            })
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON format in request body"})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
