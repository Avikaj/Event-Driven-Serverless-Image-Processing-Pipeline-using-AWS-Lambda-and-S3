import os
import json
import uuid
import boto3
from botocore.exceptions import ClientError
from PIL import Image  # Import Image from PIL

# bucketname for pixelated images
bucket_1 = os.environ['bucket_1']
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print(event)
    
    # get bucket and object key from event object
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Generate a temp name, and set location for our original image
    key_1 = str(uuid.uuid4()) + '-' + key
    download_path = '/tmp/{}'.format(key_1)
    
    # Check if the object exists in the source bucket
    try:
        s3_client.head_object(Bucket=source_bucket, Key=key)
    except ClientError as e:
        print(f"Error: Object {key} not found in bucket {source_bucket}.")
        return {
            'statusCode': 404,
            'body': json.dumps(f"Object {key} not found in bucket {source_bucket}.")
        }

    # Download the source image from S3 to temp location within execution environment
    try:
        with open(download_path, 'wb') as img_file:
            s3_client.download_fileobj(source_bucket, key, img_file)
    except ClientError as e:
        print(f"Error downloading file {key} from bucket {source_bucket}: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error downloading file: {str(e)}")
        }

    # Pixelate images in different resolutions
    try:
        pixelate((8, 8), download_path, f'/tmp/pixelated-8x8-{key_1}')
        pixelate((16, 16), download_path, f'/tmp/pixelated-16x16-{key_1}')
        pixelate((32, 32), download_path, f'/tmp/pixelated-32x32-{key_1}')
        pixelate((48, 48), download_path, f'/tmp/pixelated-48x48-{key_1}')
        pixelate((64, 64), download_path, f'/tmp/pixelated-64x64-{key_1}')
    except Exception as e:
        print(f"Error pixelating image: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error pixelating image: {str(e)}")
        }

    # Upload the pixelated versions to the destination bucket
    try:
        s3_client.upload_file(f'/tmp/pixelated-8x8-{key_1}', bucket_1, f'pixelated-8x8-{key}')
        s3_client.upload_file(f'/tmp/pixelated-16x16-{key_1}', bucket_1, f'pixelated-16x16-{key}')
        s3_client.upload_file(f'/tmp/pixelated-32x32-{key_1}', bucket_1, f'pixelated-32x32-{key}')
        s3_client.upload_file(f'/tmp/pixelated-48x48-{key_1}', bucket_1, f'pixelated-48x48-{key}')
        s3_client.upload_file(f'/tmp/pixelated-64x64-{key_1}', bucket_1, f'pixelated-64x64-{key}')
    except ClientError as e:
        print(f"Error uploading pixelated images: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error uploading pixelated images: {str(e)}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed and uploaded pixelated images.')
    }

def pixelate(pixelsize, image_path, pixelated_img_path):
    # Ensure Image module is used here
    img = Image.open(image_path)
    temp_img = img.resize(pixelsize, Image.BILINEAR)
    new_img = temp_img.resize(img.size, Image.NEAREST)
    new_img.save(pixelated_img_path)
