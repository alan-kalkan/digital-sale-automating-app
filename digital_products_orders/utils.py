def get_product_name_by_sku(event, sku):
  for line_item in event['detail']['payload']['line_items']:
    line_item_id = line_item['id']
    if line_item['sku'] == sku and line_item['id'] == line_item_id:
      return line_item['name']


def get_product_id_by_sku(event, sku):
  for line_item in event['detail']['payload']['line_items']:
    if line_item['sku'] == sku:
      return line_item['product_id']
