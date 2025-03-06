import json
import boto3
import os

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("DYNAMODB_TABLE", "ConvertedFiles")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Extract file details from S3 event
        for record in event["Records"]:
            bucket_name = record["s3"]["bucket"]["name"]
            file_key = record["s3"]["object"]["key"]  # Ex: "converted/test-sheet-event.pdf"

            # ✅ Ensure we process only converted PDF files
            if not file_key.startswith("converted/") or not file_key.endswith(".pdf"):
                print(f"Skipping non-PDF file: {file_key}")
                continue

            # ✅ Store the exact filename (NO TIMESTAMP)
            presigned_url = s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket_name, "Key": file_key},
                ExpiresIn=600  # 10 minutes expiry
            )

            # ✅ Store in DynamoDB using the exact file key
            table.put_item(Item={"file_name": file_key, "pdf_url": presigned_url})
            print(f"✅ PDF URL stored: {file_key}")

            # ✅ Delete the original .docx or .xlsx file
            base_filename = file_key.replace("converted/", "").replace(".pdf", "")
            original_extensions = [".docx", ".xlsx"]
            deleted_files = []

            for ext in original_extensions:
                original_file_key = f"uploads/{base_filename}{ext}"
                try:
                    s3.delete_object(Bucket=bucket_name, Key=original_file_key)
                    print(f"✅ Deleted original file: {original_file_key}")
                    deleted_files.append(original_file_key)
                    break  # Stop after deleting the correct file
                except s3.exceptions.ClientError as e:
                    if e.response["Error"]["Code"] == "404":
                        print(f"❌ File not found: {original_file_key}")
                    else:
                        print(f"❌ Error deleting original file ({original_file_key}): {str(e)}")

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "PDF URL stored successfully", "url": presigned_url})
        }

    except Exception as e:
        print(f"Error processing event: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
