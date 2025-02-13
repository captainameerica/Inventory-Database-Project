import streamlit as st
from database import connect_db, create_table, add_item, update_item, delete_item, get_inventory
import pandas as pd

# Connect to the database and ensure the table exists.
conn = connect_db()
create_table(conn)

st.title("PC Inventory Management System")

# Create tabs for navigation.
tab_view, tab_add, tab_update, tab_delete = st.tabs([
    "View Inventory", "Add Item", "Update Item", "Delete Item"
])

with tab_view:
    st.header("Inventory List")
    items = get_inventory(conn)
    if items:
        # Convert the list of items to a DataFrame with specified column names
        df = pd.DataFrame(items, columns=["ID", "Product Name", "Quantity", "Price"])
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No items in inventory.")

with tab_add:
    st.header("Add New Item")
    # Adding unique keys to avoid widget conflicts
    product_name = st.text_input("Product Name", key="add_product_name")
    quantity = st.number_input("Quantity", min_value=0, step=1, key="add_quantity")
    price = st.number_input("Price", min_value=0.0, step=0.1, format="%.2f", key="add_price")
    if st.button("Add", key="add_button"):
        if product_name and quantity and price:
            add_item(conn, product_name, quantity, price)
            st.success("Item added successfully!")
        else:
            st.error("Please provide all item details.")

with tab_update:
    st.header("Update Existing Item")
    item_id_str = st.text_input("Item ID to Update", key="update_item_id")
    new_name = st.text_input("New Product Name (leave blank to keep unchanged)", key="update_new_name")
    new_quantity_str = st.text_input("New Quantity (leave blank to keep unchanged)", key="update_new_quantity")
    new_price_str = st.text_input("New Price (leave blank to keep unchanged)", key="update_new_price")
    if st.button("Update", key="update_button"):
        try:
            item_id = int(item_id_str)
            new_quantity = int(new_quantity_str) if new_quantity_str.strip() != "" else None
            new_price = float(new_price_str) if new_price_str.strip() != "" else None
            update_item(conn, item_id, new_name or None, new_quantity, new_price)
            st.success("Item updated successfully!")
        except ValueError:
            st.error("Please enter a valid Item ID and numeric values for Quantity/Price.")

with tab_delete:
    st.header("Delete Item")
    item_id_str = st.text_input("Item ID to Delete", key="delete_item_id")
    if st.button("Delete", key="delete_button"):
        try:
            item_id = int(item_id_str)
            delete_item(conn, item_id)
            st.success("Item deleted successfully!")
        except ValueError:
            st.error("Please enter a valid Item ID.")
