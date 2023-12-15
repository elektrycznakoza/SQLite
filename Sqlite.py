import sqlite3
import datetime

# Funkcja do tworzenia połączenia z bazą danych
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Utworzono połączenie z bazą danych: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Funkcja do wykonania zapytania SQL
def execute_sql(conn, sql, message):
    try:
        c = conn.cursor()
        c.execute(sql)
        print(f"{message}: Wykonano pomyślnie zapytanie SQL.")
        # Logowanie wykonanych operacji do pliku
        with open('sqlitecheck.txt', 'a') as log_file:
            log_file.write(f"{datetime.datetime.now()} - {message}\n")
    except sqlite3.Error as e:
        print(e)

# Funkcja do usuwania i resetowania tabel
def delete_and_reset_tables(conn):
    user_input = input("Czy chcesz usunąć i zresetować tabele? (tak/nie): ")
    if user_input.lower() == 'tak':
        execute_sql(conn, "DROP TABLE IF EXISTS projects;", "Usuwanie tabeli projects")
        execute_sql(conn, "DROP TABLE IF EXISTS tasks;", "Usuwanie tabeli tasks")

# Funkcja do dodawania projektu do bazy danych
def add_project(conn, project):
    sql = '''INSERT INTO projects(nazwa, start_date, end_date, priority, responsible_person)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    print(f"Dodano nowy projekt o ID {cur.lastrowid}")
    # Logowanie wykonanych operacji do pliku
    with open('sqlitecheck.txt', 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - Dodano nowy projekt o ID {cur.lastrowid}\n")
    return cur.lastrowid

# Funkcja do dodawania zadania do bazy danych
def add_task(conn, task):
    sql = '''INSERT INTO tasks(project_id, nazwa, opis, status, start_date, end_date, priority, responsible_person)
             VALUES(?,?,?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    print(f"Dodano nowe zadanie o ID {cur.lastrowid}")
    # Logowanie wykonanych operacji do pliku
    with open('sqlitecheck.txt', 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - Dodano nowe zadanie o ID {cur.lastrowid}\n")
    return cur.lastrowid

# Funkcja do wyświetlania struktury tabeli
def print_table_structure(conn, table_name):
    query = f"PRAGMA table_info({table_name});"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Struktura tabeli {table_name}:")
    for row in rows:
        print(row)

# Funkcja do filtrowania projektów według osoby odpowiedzialnej
def filter_projects_by_responsible_person(conn, person):
    query = f"SELECT * FROM projects WHERE responsible_person = '{person}';"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Projekty przypisane osobie {person}:")
    for row in rows:
        print(row)

# Funkcja do filtrowania zadań według priorytetu "High"
def filter_tasks_by_priority(conn, priority):
    query = f"SELECT * FROM tasks WHERE priority = '{priority}';"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print(f"Zadania o priorytecie {priority}:")
    for row in rows:
        print(row)

# Główna część kodu
if __name__ == "__main__":
    # Utworzenie połączenia z bazą danych
    conn = create_connection("database.db")
    if conn is not None:
        # Usunięcie i zresetowanie tabel, jeśli użytkownik wyrazi zgodę
        delete_and_reset_tables(conn)

        # Utworzenie tabel projects i tasks, jeśli nie istnieją
        execute_sql(conn, "CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, nazwa TEXT NOT NULL, start_date TEXT, end_date TEXT, priority TEXT, responsible_person TEXT);", "Tworzenie tabeli projects")
        execute_sql(conn, "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, project_id INTEGER NOT NULL, nazwa VARCHAR(250) NOT NULL, opis TEXT, status VARCHAR(15) NOT NULL, start_date TEXT NOT NULL, end_date TEXT NOT NULL, priority TEXT, responsible_person TEXT, UNIQUE(project_id, nazwa, start_date));", "Tworzenie tabeli tasks")

        # Dane testowe dla projektów
        projects = [
            ("Projekt A", "2023-01-01 00:00:00", "2023-01-10 00:00:00", "High", "Leszek"),
            ("Projekt B", "2023-02-01 00:00:00", "2023-02-15 00:00:00", "Medium", "Anna"),
            ("Projekt C", "2023-03-01 00:00:00", "2023-03-10 00:00:00", "Low", "Jan")
        ]

        # Dane testowe dla zadań
        tasks = [
            (1, "Zadanie A1", "Opis zadania A1", "started", "2023-01-01 08:00:00", "2023-01-01 12:00:00", "High", "Leszek"),
            (2, "Zadanie A2", "Opis zadania A2", "completed", "2023-01-05 10:00:00", "2023-01-05 14:00:00", "Low", "Jan"),
            (3, "Zadanie B1", "Opis zadania B1", "started", "2023-02-01 09:00:00", "2023-02-01 13:00:00", "Medium", "Anna"),
            (4, "Zadanie B2", "Opis zadania B2", "completed", "2023-02-10 11:00:00", "2023-02-10 15:00:00", "High", "Leszek"),
            (5, "Zadanie C1", "Opis zadania C1", "started", "2023-03-01 08:00:00", "2023-03-01 12:00:00", "Medium", "Anna"),
            (6, "Zadanie C2", "Opis zadania C2", "completed", "2023-03-05 10:00:00", "2023-03-05 14:00:00", "Low", "Jan"),
            (7, "Zadanie C3", "Opis zadania C3", "started", "2023-03-08 09:00:00", "2023-03-08 13:00:00", "High", "Leszek"),
            (8, "Zadanie C4", "Opis zadania C4", "completed", "2023-03-10 11:00:00", "2023-03-10 15:00:00", "Medium", "Anna")
        ]

        # Dodanie projektów do bazy danych
        for project_data in projects:
            pr_id = add_project(conn, project_data)

        # Dodanie zadań do bazy danych
        for task_data in tasks:
            task_id = add_task(conn, task_data)

        # Wyświetlenie struktury tabel
        print_table_structure(conn, 'projects')
        print_table_structure(conn, 'tasks')

        # Filtrowanie projektów i zadań oraz wyświetlenie wyników
        filter_projects_by_responsible_person(conn, 'Leszek')
        filter_tasks_by_priority(conn, 'High')

        # Zamknięcie połączenia z bazą danych
        conn.commit()
        conn.close()
        print("Zamknięto połączenie z bazą danych")
