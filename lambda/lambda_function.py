import boto3
import json
import os
from botocore.client import Config

s3 = boto3.client("s3", config=Config(signature_version="s3v4"))

# Bucket privado donde se guardan los archivos subidos desde la web
BUCKET = os.environ.get("BUCKET_NAME", "miguel-privado0")


def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    nombre = params.get("archivo")

    if not nombre:
        return {
            "statusCode": 400,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"error": "Falta el parametro 'archivo'"}),
        }

    url = s3.generate_presigned_url(
        ClientMethod="put_object",
        Params={"Bucket": BUCKET, "Key": nombre},
        ExpiresIn=300,  # la URL vale 5 minutos
    )

    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": "*"},
        "body": json.dumps({"url": url}),
    }
