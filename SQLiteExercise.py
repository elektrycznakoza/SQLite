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
        execute_sql(conn, "DROP TABLE IF EXISTS projects;")
        execute_sql(conn, "DROP TABLE IF EXISTS tasks;")

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

def update_data(conn, table, task_id, **kwargs):
    """Aktualizuje dane w tabeli."""
    parameters = [f"{k} = ?" for k in kwargs]
    parameters = ", ".join(parameters)
    values = tuple(v for v in kwargs.values())
    values += (task_id, )

    sql = f"UPDATE {table} SET {parameters} WHERE id = ?"
    try:
        cur = conn.cursor()
        cur.execute(sql, values)
        conn.commit()
        print(f"Data updated successfully in {table} table.")
    except Error as e:
        print(e)

def delete_task(conn, task_id):
    try:
        task_details = select_all(conn, "tasks", "id = ?", (task_id,))
        if not task_details:
            print(f"Task with id {task_id} not found.")
            return

        task_details = task_details[0] 
        task_name = task_details[2] 

        sql = "DELETE FROM tasks WHERE id = ?"
        cur = conn.cursor()
        cur.execute(sql, (task_id,))
        conn.commit()

        print(f"Task '{task_name}' (ID: {task_id}) deleted successfully from tasks table.")
    except Error as e:
        print(e)

if __name__ == "__main__":
    db_file = "database.db"

    conn = create_connection(db_file)

    delete_and_reset_tables(conn)

    create_projects_sql = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL
    );
    """

    create_tasks_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        project_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        description TEXT,
        status TEXT NOT NULL,
        start_date TEXT NOT NULL,
        end_date TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    """

    create_table(conn, create_projects_sql)
    create_table(conn, create_tasks_sql)

    project_data = (1, 'Letnia Promocja 2022', 'Przygotowanie i realizacja letniej kampanii promocyjnej dla produktów firmy.', 'W trakcie', '2022-06-01', '2022-08-31')
    task_data = (1, 1, 'Przygotowanie Materiałów Promocyjnych', 'Stworzenie atrakcyjnych grafik i treści reklamowych.', 'Zakończone', '2022-06-01', '2022-06-15')

    insert_data(conn, "INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)", project_data, "projects")
    insert_data(conn, "INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)", task_data, "tasks")

    new_project_data = (2, 'Zimowa Kampania 2023', 'Przygotowanie i realizacja zimowej kampanii promocyjnej dla produktów firmy.', 'Planowane', '2023-01-01', '2023-02-28')
    insert_data(conn, "INSERT INTO projects VALUES (?, ?, ?, ?, ?, ?)", new_project_data, "projects")

    print("\nWszystkie projekty po dodaniu nowego:")
    print(select_all(conn, "projects"))

    updated_task_data = {
        "name": "Nowe Zadanie",
        "status": "W trakcie",
        "end_date": "2023-01-15"
    }
    update_data(conn, "tasks", 1, **updated_task_data)

    print("\nWszystkie zadania po aktualizacji:")
    print(select_all(conn, "tasks", "project_id = ?", (1,)))

    delete_task_id = 1
    delete_task(conn, delete_task_id)

    print("\nWszystkie projekty po usunięciu:")
    print(select_all(conn, "projects"))

    print("\nWszystkie zadania po usunięciu:")
    print(select_all(conn, "tasks"))

    if conn:
        conn.close()
        print("Connection closed")
