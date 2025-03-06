import json
import boto3
import os
import urllib.parse

dynamodb = boto3.resource("dynamodb")
table_name = os.environ.get("DYNAMODB_TABLE", "ConvertedFiles")
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Extract and decode file name
        if "queryStringParameters" not in event or "file_name" not in event["queryStringParameters"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing file_name parameter"})
            }

        file_name = event["queryStringParameters"]["file_name"]
        decoded_file_name = urllib.parse.unquote(file_name)  # Decode before querying

        # Query DynamoDB for exact match
        response = table.get_item(Key={"file_name": decoded_file_name})

        if "Item" not in response:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "File not found in database"})
            }

        pdf_url = response["Item"]["pdf_url"]
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "PDF URL found", "url": pdf_url})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
