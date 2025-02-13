import streamlit as st
from database import connect_db, create_table, add_item, update_item, delete_item, get_inventory
import pandas as pd
# Connect to the database and ensure the table exists.
conn = connect_db()
create_table(conn)

st.title("Inventory Management System")

# Sidebar navigation for different operations.
menu = ["View Inventory", "Add Item", "Update Item", "Delete Item"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "View Inventory":
    st.header("Inventory List")
    items = get_inventory(conn)
    if items:
        # Convert the list of items to a DataFrame with specified column names
        df = pd.DataFrame(items, columns=["ID", "Product Name", "Quantity", "Price"])
        st.dataframe(df)
    else:
        st.write("No items in inventory.")

elif choice == "Add Item":
    st.header("Add New Item")
    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=0, step=1)
    price = st.number_input("Price", min_value=0.0, step=0.1, format="%.2f")
    if st.button("Add"):
        if product_name and quantity and price:
            add_item(conn, product_name, quantity, price)
            st.success("Item added successfully!")
        else:
            st.error("Please provide all item details.")

elif choice == "Update Item":
    st.header("Update Existing Item")
    item_id_str = st.text_input("Item ID to Update")
    new_name = st.text_input("New Product Name (leave blank to keep unchanged)")
    new_quantity_str = st.text_input("New Quantity (leave blank to keep unchanged)")
    new_price_str = st.text_input("New Price (leave blank to keep unchanged)")

    if st.button("Update"):
        try:
            item_id = int(item_id_str)
            new_quantity = int(new_quantity_str) if new_quantity_str.strip() != "" else None
            new_price = float(new_price_str) if new_price_str.strip() != "" else None
            update_item(conn, item_id, new_name or None, new_quantity, new_price)
            st.success("Item updated successfully!")
        except ValueError:
            st.error("Please enter a valid Item ID and numeric values for Quantity/Price.")

elif choice == "Delete Item":
    st.header("Delete Item")
    item_id_str = st.text_input("Item ID to Delete")
    if st.button("Delete"):
        try:
            item_id = int(item_id_str)
            delete_item(conn, item_id)
            st.success("Item deleted successfully!")
        except ValueError:
            st.error("Please enter a valid Item ID.")
