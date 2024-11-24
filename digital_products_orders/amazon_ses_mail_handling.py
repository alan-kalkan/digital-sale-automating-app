from collections import defaultdict
import boto3
from botocore.exceptions import ClientError
from html_variables import mail_body
from queries import check_sku_exists, check_code_exists, update_email_status
def send_mail_ses(connexion, event, firstName, orderId, email):
    AWS_REGION = "eu-west-3"
    codes = check_code_exists(connexion, orderId)
    if not codes:
        return
    else:
        line_items_by_vendor = defaultdict(list)

        skus_from_event = []
        lineItemIds_from_event = []
        productIds_from_event = []
        quantity_per_line_item_from_event = []
        products_title_from_event = []
    
        for line_item in event['detail']['payload']['line_items']:
            sku = line_item['sku']
            if check_sku_exists(connexion, sku):
                skus_from_event.append(line_item['sku'])
                lineItemIds_from_event.append(line_item['id'])
                vendor = line_item["vendor"]
                line_items_by_vendor[vendor].append(line_item)
                productIds_from_event.append(line_item['product_id'])
                quantity_per_line_item_from_event.append(line_item['fulfillable_quantity'])
                products_title_from_event.append(line_item['name'])

        
        client = boto3.client('ses', region_name=AWS_REGION)


        for vendor, line_items in line_items_by_vendor.items():
                product_id = [line_item['product_id'] for line_item in line_items]
                product_title = [line_item['name'] for line_item in line_items]
                skus = [line_item['sku'] for line_item in line_items]
                line_items_id = [line_item['id'] for line_item in line_items]
                
                BODY_HTML = mail_body(event, connexion, firstName, vendor, product_id, product_title, skus, line_items_id)
                RECIPIENT = email
                CHARSET = "UTF-8"
                SENDER = "donotreply@thebradery.com"
                
                SUBJECT = f"Vos codes de votre commande {vendor}"
                BODY_TEXT = ("Hey Hi...\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                 )
                try:
                    response = client.send_email(
                        Destination={
                            'ToAddresses': [
                                RECIPIENT,
                            ],
                        },
                        Message={
                            'Body': {
                                'Html': {
                                    'Data': BODY_HTML
                                },
                                'Text': {
                                    'Data': BODY_TEXT
                                },
                            },
                            'Subject': {
                                'Data': SUBJECT
                            },
                        },
                        Source=SENDER
                    )
                    print(f"Email sent for order {orderId}! Message ID:", response['MessageId'])
                except:
                    print(f"Email sending failed for order {orderId}")
        try:
            update_email_status(connexion, orderId)
        except Exception as e:
            print('Error while updating the mail status:', e)
