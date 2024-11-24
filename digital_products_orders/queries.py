import mysql.connector
import uuid
from shopify_data import retrieve_order_name

def get_available_digital_code(connexion, sku):
    available_codes = []
    try:
        cursor = connexion.cursor(buffered=True)
        
        sql = """
        SELECT code  
        FROM thebradery.digital_products 
        LEFT JOIN thebradery.digital_products_orders
        ON digital_products.code = digital_products_orders.digitalProductCode 
        WHERE digital_products.sku = %s AND digitalProductCode IS NULL
        """
        
        cursor.execute(sql, (sku,))
        rows = cursor.fetchall()
        
        for row in rows:
            available_codes.append(row[0]) 

        return available_codes
    
    except mysql.connector.Error as err:
        print("Error:", err)

def check_line_item_exists(connexion, lineItem_Id):
    cursor = connexion.cursor(buffered=True)
    try:
        query = "SELECT COUNT(*) FROM thebradery.digital_products_orders WHERE line_item_id = %s"
        cursor.execute(query, (lineItem_Id,))
        count = cursor.fetchone()[0]
        return count > 0
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

def check_sku_exists(connexion, sku):
    cursor = connexion.cursor(buffered=True)
    try:
        query = "SELECT COUNT(*) FROM thebradery.digital_products WHERE sku = %s"
        cursor.execute(query, (sku,))
        count = cursor.fetchone()[0]
        return count > 0
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

def insert_digital_orders(connexion, orderId, line_item_ids, skus, quantity):
    cursor = connexion.cursor(buffered=True)
    order_number = retrieve_order_name(orderId)
    try:
        for lineItemId, sku, quant in zip(line_item_ids, skus, quantity):
            digital_product = check_sku_exists(connexion, sku) ## Only adding the digital products into the database
            if digital_product:
                available_codes = get_available_digital_code(connexion, sku)
                if available_codes:
                    insert_sql = """
                        INSERT INTO thebradery.digital_products_orders (id, orderId, line_item_id, digitalProductCode, sku, orderNumber)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    for _ in range(quant):
                        id = uuid.uuid4()
                        for digital_code in available_codes:
                            try:
                                cursor.execute(insert_sql, (str(id), orderId, lineItemId, digital_code, sku, order_number))
                                connexion.commit()
                                print(f"Order: {orderId} inserted into databse")
                                break
                            except mysql.connector.Error as err:
                                if err.errno == 1062: ## This error occurs when a code is assimilated to an order more than one time (whereas each code is unique)
                                    attempt = 1
                                    while attempt <= 10:
                                        try:
                                            cursor.execute(insert_sql, (str(id), orderId, lineItemId, digital_code, sku, order_number))
                                            connexion.commit()
                                            print(f"Order {orderId} inserted into database, attempt number {attempt}")
                                            break
                                        except mysql.connector.Error as err:
                                            print(err)
                                            break
                                else:
                                    print(f"Error inserting [SKU: {sku}; CODE : {digital_code}] for order {orderId}")
                                    connexion.rollback()
                                    break
                else:
                    insert_if_out_of_code_sql = """
                    INSERT INTO thebradery.digital_products_orders (id, orderId, line_item_id, digitalProductCode, sku, orderNumber) VALUES (%s ,%s ,%s ,%s, %s);
                """
                    for _ in range(quant):
                        id = uuid.uuid4()
                        cursor.execute(insert_if_out_of_code_sql, (str(id), orderId, lineItemId, sku, order_number))
                        connexion.commit()
                        print(f"Order {orderId} inserted but out of code")
    except mysql.connector.Error as err:
        print("Error:", err)
        connexion.rollback()

def select_codes_from_lineItem(connexion, line_item_id):
    cursor = connexion.cursor(buffered=True)
    result = []  
    try:
        select_sql = """
        SELECT 
            sku,
            digitalProductCode
        FROM
            thebradery.digital_products_orders
        WHERE
            line_item_id = %s
        """
        cursor.execute(select_sql, (line_item_id,))
        rows = cursor.fetchall()
        for row in rows:
            result.append(row)
    except mysql.connector.Error as err:
        print("Error:", err)
        connexion.rollback()
    return result

def select_codes_from_orderId(connexion, orderId):
    
    cursor = connexion.cursor(buffered=True)
    result = []  
    try:
        select_sql = """
        SELECT 
        digitalProductCode, sku
    FROM
        thebradery.digital_products_orders
    WHERE
        orderId = %s
        """
        cursor.execute(select_sql, (orderId,))
        rows = cursor.fetchall()
        for row in rows:
                result.append(row)
    except mysql.connector.Error as err:
            print("Error:", err)
            connexion.rollback()
    return result
    
def check_code_exists(connexion, orderId):
    
    cursor = connexion.cursor(buffered=True)
    result = [] 
    try:
        select_sql = """
        SELECT 
        digitalProductCode
    FROM
        thebradery.digital_products_orders
    WHERE
        orderId = %s
        """
        cursor.execute(select_sql, (orderId,))
        rows = cursor.fetchall()
        for row in rows:
                result.append(row)
    except mysql.connector.Error as err:
            print("Error:", err)
            
    return result

def update_email_status(connexion, orderId):
        cursor = connexion.cursor(buffered=True)
        cursor.execute("SET SQL_SAFE_UPDATES = 0;")
        
        update_query = """
        UPDATE thebradery.digital_products_orders
        SET email_sent = 1
        WHERE orderId = %s;
        """
        cursor.execute(update_query, (orderId,))
        cursor.execute("SET SQL_SAFE_UPDATES = 1;")
        connexion.commit()