import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, SQLite version: {sqlite3.version}")
        return conn
    except Error as e:
        print(e)

def delete_and_reset_tables(conn):
    user_input = input("Czy chcesz usunąć i zresetować tabele? (tak/nie): ")
    if user_input.lower() == 'tak':
        execute_sql(conn, "DROP TABLE IF EXISTS customers;")
        execute_sql(conn, "DROP TABLE IF EXISTS orders;")

def execute_sql(conn, sql, data=None):
    try:
        cur = conn.cursor()
        if data:
            cur.execute(sql, data)
        else:
            cur.execute(sql)
        return cur
    except Error as e:
        print(e)

def create_table(conn, create_table_sql):
    try:
        execute_sql(conn, create_table_sql)
        print("Table created successfully")
    except Error as e:
        print(e)

def insert_data(conn, insert_sql, data, table):
    try:
        cur = conn.cursor()
        cur.execute(insert_sql, data)
        conn.commit()
        print(f"Data inserted successfully into {table} table.")
    except Error as e:
        print(e)

def select_all(conn, table, conditions=None, params=None):
    try:
        cur = conn.cursor()
        if conditions:
            cur.execute(f"SELECT * FROM {table} WHERE {conditions}", params)
        else:
            cur.execute(f"SELECT * FROM {table}")
        rows = cur.fetchall()
        return rows
    except Error as e:
        print(e)

def update_data(conn, table, order_id, **kwargs):
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (order_id, )

    sql = f"UPDATE {table} SET {parameters} WHERE id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print(f"Data updated successfully in {table} table.")
    except Error as e:
        print(e)

def delete_order(conn, order_id):
    try:
        order_details = select_all(conn, "orders", "id = ?", (order_id,))
        if not order_details:
            print(f"Order with id {order_id} not found.")
            return

        order_details = order_details[0] 
        product_name = order_details[2] 

        sql = "DELETE FROM orders WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql, (order_id,))
        conn.commit()

        print(f"Order '{product_name}' (ID: {order_id}) deleted successfully from orders table.")
    except Error as e:
        print(e)

if __name__ == "__main__":
    db_file = "database.db"

    conn = create_connection(db_file)

    delete_and_reset_tables(conn)

    create_customers_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT
    );
    """

    create_orders_sql = """
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY,
        customer_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (id)
    );
    """

    create_table(conn, create_customers_sql)
    create_table(conn, create_orders_sql)

    customer_data = (1, 'John Doe', 'john@example.com', '123-456-7890')
    order_data = (1, 1, 'Dark chocolate', 2, 19.99)

    insert_data(conn, "INSERT INTO customers VALUES (?, ?, ?, ?)", customer_data, "customers")
    insert_data(conn, "INSERT INTO orders VALUES (?, ?, ?, ?, ?)", order_data, "orders")

    new_customer_data = (2, 'Jane Smith', 'jane@example.com', '987-654-3210')
    insert_data(conn, "INSERT INTO customers VALUES (?, ?, ?, ?)", new_customer_data, "customers")

    print("\nWszyscy klienci po dodaniu nowego:")
    print(select_all(conn, "customers"))

    nowe_zamowienia = [
        (2, 1, 'Chleb pszenny', 1, 3.50),
        (3, 2, 'Ser pleśniowy', 2, 12.99),
        (4, 1, 'Mleko pełnotłuste', 3, 2.99)
    ]

    insert_sql = "INSERT INTO orders VALUES (?, ?, ?, ?, ?)"
    for zamowienie in nowe_zamowienia:
        insert_data(conn, insert_sql, zamowienie, "orders")

    print("\nWszystkie zamówienia po aktualizacji:")
    print(select_all(conn, "orders", "customer_id = ?", (1,)))

    delete_order_id = 1
    delete_order(conn, delete_order_id)

    print("\nWszyscy klienci po usunięciu:")
    print(select_all(conn, "customers"))

    print("\nWszystkie zamówienia po usunięciu:")
    print(select_all(conn, "orders"))

    if conn:
        conn.close()
        print("Connection closed")
