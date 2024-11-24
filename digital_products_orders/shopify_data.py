import requests
import shopify
import binascii
import os
import json
import asyncio
import boto3

secret_name = "tb/prod/shopify-INT-OPS-credentials"
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

aws_api_key = secret_data["SHOPIFY_APP_API_KEY"]
aws_api_secret = secret_data["SHOPIFY_APP_API_SECRET"]
aws_secret_token = secret_data["SHOPIFY_APP_API_ACCES_TOKEN"]

shop_url = "my-moon-store.myshopify.com"
api_version = '2024-01'

def retrieve_shopify_data(product_id):

  shopify.Session.setup(api_key=aws_api_key, secret=aws_api_secret)
  session = shopify.Session(shop_url, api_version, aws_secret_token)
  shopify.ShopifyResource.activate_session(session)

  graphql_query = f"""
    query {{
      product(id: "gid://shopify/Product/{product_id}") {{
        metafields(first: 10) {{
          edges {{
            node {{
              namespace
              key
              value
            }}
          }}
        }}
        vendor
      }}
    }}
  """
  
  try: 
    graphql_response = shopify.GraphQL().execute(graphql_query)
    graphql_data = json.loads(graphql_response)
    
    metafields_values = []
    metafields = graphql_data.get("data", {}).get("product", {}).get("metafields", {}).get("edges", [])
    for edge in metafields:
          key = edge["node"]["key"]
          value = edge["node"]["value"]
          if key in ["description_infos_1", "description_infos_2", "return_policy"]:
              metafields_values.append(value)
    shopify.ShopifyResource.clear_session()
    return metafields_values
  except Exception as e:
    print("Error while retrieving metafields, they might not exist:", e)
    pass

def create_order_metafield(data, order_id):
  if data == [] or data == None:
    return
  else:
    shopify.Session.setup(api_key=aws_api_key, secret=aws_api_secret)
    session = shopify.Session(shop_url, api_version, aws_secret_token)
    shopify.ShopifyResource.activate_session(session)
    
    dict = {"codes" : {}}

    for c, s in data:
            if s in dict["codes"]:
                dict["codes"][s].append(c)
            else:
                dict["codes"][s] = [c]

    
  
    metafield_value = json.dumps(dict).replace('"', r'\"')
    graphql_query = """
        mutation {
          orderUpdate(
          input : {
            id: "gid://shopify/Order/%s",
            metafields: [
              {
                namespace: "custom",
                key: "codes",
                value: "%s",
                type: "json",
              }
            ]
          }) {
            order {
              metafields(first: 100) {
                edges {
                  node {
                    namespace
                    key
                    value
                  }
                }
              }
            }
          }
        }
    """ % (order_id, metafield_value)
    
    graphql_response = shopify.GraphQL().execute(graphql_query)
    graphql_data = json.loads(graphql_response)
    shopify.ShopifyResource.clear_session()
    print(f"Metafield created for order {order_id}")

def retrieve_product_title(productId):
    shopify.Session.setup(api_key=aws_api_key, secret=aws_api_secret)
    session = shopify.Session(shop_url, api_version, aws_secret_token)
    shopify.ShopifyResource.activate_session(session)
    
    graphql_query = f"""
query {{
  product(id: "gid://shopify/Product/{productId}") {{
    title
    description
    onlineStoreUrl
  }}
}}
    """
    graphql_response = shopify.GraphQL().execute(graphql_query)
    graphql_data = json.loads(graphql_response)
    product_title = graphql_data.get("data", {}).get("product", {}).get("title", {})
    return product_title
  
def retrieve_order_name(orderId):
  shopify.Session.setup(api_key=aws_api_key, secret=aws_api_secret)
  session = shopify.Session(shop_url, api_version, aws_secret_token)
  shopify.ShopifyResource.activate_session(session)
    
  graphql_query = f"""
    query {{
      node(id: "gid://shopify/Order/{orderId}") {{
        id
        ... on Order {{
          name
        }}
      }}
    }}
    """
  graphql_response = shopify.GraphQL().execute(graphql_query)
  graphql_data = json.loads(graphql_response)
  order_name = graphql_data.get("data", {}).get("node", {}).get("name", {}).split("#")[1]
  return order_name
