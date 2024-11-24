import mysql.connector

def insert_digital_products(connexion, data, productVendor):
    cursor = connexion.cursor(buffered=True)
    sql = "INSERT INTO thebradery.digital_products (sku, code, productVendor) VALUES (%s, %s, %s)"
    for row in data:
        sku = row[0]
        codes = row[1:]
        for code in codes:
            try:
                if isinstance(code, str):
                    cursor.execute(sql, (sku, code, productVendor))
                connexion.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}. Skipping [{sku} : {code}]")
                connexion.rollback()
                continue
    cursor.close()