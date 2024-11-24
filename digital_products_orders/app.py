from collections import defaultdict
import json
import boto3
import json
import mysql.connector
from queries import insert_digital_orders, select_codes_from_orderId, check_sku_exists
from amazon_ses_mail_handling import send_mail_ses
from shopify_data import create_order_metafield

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
                app_staging_db = mysql.connector.connect(
                    host=aws_host,
                    user=aws_username,
                    password=aws_password,
                    database=aws_db_name
                )
                print('connected',app_staging_db)
                return app_staging_db
            except mysql.connector.Error as err:
                print("Error:", err)
                return None


# This lambda handles webhook events for new digital product orders, assigning unique codes to each order and storing them in the database.
def lambda_handler(event, context):
    connexion = dbConnexion(aws_host, aws_username, aws_password, aws_db_name)
    
    skus_from_event = []
    lineItemIds_from_event = []
    vendors_from_event= []
    productIds_from_event = []
    quantity_per_line_item_from_event = []
    products_title_from_event = []
    
    orderId_from_event = event['detail']['payload']['id']
    customer_firstName_from_event = event['detail']['payload']['customer']['first_name']
    customer_mail_from_event = event['detail']['payload']['customer']['email']
    for line_item in event['detail']['payload']['line_items']:
        sku = line_item['sku']
        if check_sku_exists(connexion, sku):
            skus_from_event.append(sku)
            lineItemIds_from_event.append(line_item['id'])
            productIds_from_event.append(line_item['product_id'])
            quantity_per_line_item_from_event.append(line_item['fulfillable_quantity'])
            products_title_from_event.append(line_item['name'])

    try:
        insert_digital_orders(connexion, orderId_from_event, lineItemIds_from_event, skus_from_event, quantity_per_line_item_from_event)
        send_mail_ses(connexion, event, customer_firstName_from_event, orderId_from_event, customer_mail_from_event)
        data = select_codes_from_orderId(connexion, orderId_from_event)
        create_order_metafield(data, orderId_from_event)
    except Exception as e:
        print(f'Error : {e}, order {orderId_from_event} skipped')
        
            
    return {
    "statusCode": 200,
    "body": json.dumps({
                    "message": "Lambda end", })},


   