from config import get_db_connection
import pyodbc
from datetime import datetime

def get_db_connection():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=DESKTOP-E7TMHHH;'
        'DATABASE=python_crud;'
        'UID=sa;'
        'PWD=admin123;'
        'Encrypt=no;'
        'TrustServerCertificate=yes;'
    )
    return conn

# Funciones CRUD para productos
def get_all_items():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, quantity FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

def get_item_by_id(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, price, quantity FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def create_item(name, description, price, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description, price, quantity) VALUES (?, ?, ?, ?)", (name, description, price, quantity))
    conn.commit()
    conn.close()

def update_item(item_id, name, description, price, quantity):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, description = ?, price = ?, quantity = ? WHERE id = ?", (name, description, price, quantity, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def get_paginated_items(page, per_page):
    conn = get_db_connection()
    cursor = conn.cursor()
    offset = (page - 1) * per_page
    cursor.execute("SELECT id, name, description, price, quantity FROM items ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", (offset, per_page))
    items = cursor.fetchall()
    conn.close()
    return items

def get_total_items_count():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM items")
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Funciones para manejar cargas de archivos
def log_file_upload(filename, product_count):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO file_uploads (filename, upload_date, product_count) VALUES (?, ?, ?)",
                   (filename, datetime.now(), product_count))
    conn.commit()
    conn.close()

def get_all_file_uploads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, upload_date, product_count FROM file_uploads ORDER BY upload_date DESC")
    uploads = cursor.fetchall()
    conn.close()
    return uploads

def delete_file_upload(upload_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM file_uploads WHERE id = ?", (upload_id,))
    conn.commit()
    conn.close()

def delete_file_uploads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM file_uploads")
    cursor.execute("DELETE FROM items")
    conn.commit()
    conn.close()