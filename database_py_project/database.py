import sqlite3

def connect_db(db_name="my_database.db"):
    conn = sqlite3.connect(db_name)
    return conn

def create_table(conn):

    with conn:
        conn.execute(

        )
    print("Inventory table is ready.")

def add_item(conn,product_name, quantity,price):
    with conn:
        conn.execute(
            "INSERT INTO inventory (product_name, quantity, price) VALUES (?, ?, ?)",

            (product_name, quantity, price)
        )
    print(f"Added item: {product_name}")

def update_item(conn,item_id, product_name=None, quantity=None, price=None):

    updates = []
    parameters = []
    if product_name is not None:
        updates.append("product_Name = ?")
        parameters.append(product_name)
    if quantity is not None:
        updates.append("quantity = ?")
        parameters.append(quantity)
    if price is not None:
        updates.append("price = ?")
        parameters.append(price)

    if updates:
        parameters.append(item_id)
        with conn:
            conn.execute(f"UPDATE inventory SET {', '.join(updates)} WHERE id = ?", parameters)
        print(f"Updated item id: {item_id}")

def delete_item(conn, item_id):
    """Delete an item from the inventory."""
    with conn:
        conn.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
    print(f"Deleted item id: {item_id}")

def get_inventory(conn):
    """Retrieve all items from the inventory."""
    cursor = conn.cursor()
    cursor.execute("SELECT id, product_name, quantity, price FROM inventory")
    return cursor.fetchall()