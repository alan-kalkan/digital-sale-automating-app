import json
import pandas as pd 
import boto3
import io
import json
import boto3
import mysql.connector

from queries import insert_digital_products

secret_name = "tb-app/database/prod"
region_name = "eu-west-3"

session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)

get_secret_value_response = client.get_secret_value(
SecretId=secret_name
)
secret = get_secret_value_response['SecretString']
secret_data = json.loads(secret)
aws_username = secret_data['username']
aws_password = secret_data['password']
aws_host = secret_data['host']
aws_db_name = secret_data['db']

def dbConnexion(aws_host, aws_username, aws_password, aws_db_name):
 try: 
  app_prod_db = mysql.connector.connect(
   host=aws_host,
   user=aws_username,
   password=aws_password,
   database=aws_db_name
  )
  print('connected',app_prod_db)
  return app_prod_db
 except mysql.connector.Error as err:
  print("Error:", err)
  return None

## This lambda is triggered when receiving an excel file in the s3 bucket, retrieving the content and inserting it into the database
def lambda_handler(event, context):
    connexion = dbConnexion(aws_host, aws_username, aws_password, aws_db_name)

    if 'Records' in event:
        for record in event['Records']:
            if record['eventSource'] == 'aws:s3':
                bucket_name = record['s3']['bucket']['name']
                file_key = record['s3']['object']['key']
                s3 = boto3.client('s3')
                file_obj = s3.get_object(Bucket=bucket_name, Key=file_key)
                
                if file_key.endswith('.xlsx') or file_key.endswith('.xls'):
                    product_vendor = file_key.split('.')[0]               
                    excel_data = pd.read_excel(io.BytesIO(file_obj['Body'].read()), header=None)
                    row = excel_data.values.tolist()
                    insert_digital_products(connexion, row, product_vendor)
                    connexion.close()
                    print("Codes inserted successfully")
    else: 
        print("Error while uploading the file into the databse")
        
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Data inserted into the table",
        }),
    }