import sqlite3
import datetime

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Utworzono połączenie z bazą danych: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

def execute_sql(conn, sql, message):
    try:
        c = conn.cursor()
        c.execute(sql)
        print(f"{message}: Wykonano pomyślnie zapytanie SQL.")
        with open('sqlitecheck.txt', 'a') as log_file:
            log_file.write(f"{datetime.datetime.now()} - {message}\n")
    except sqlite3.Error as e:
        print(e)

def delete_and_reset_tables(conn):
    user_input = input("Czy chcesz usunąć i zresetować tabele? (tak/nie): ")
    if user_input.lower() == 'tak':
        execute_sql(conn, "DROP TABLE IF EXISTS premier_league;", "Usuwanie tabeli premier_league")
        execute_sql(conn, "DROP TABLE IF EXISTS top_scorers;", "Usuwanie tabeli top_scorers")

def add_team(conn, team_data):
    sql = '''INSERT INTO premier_league(miejsce, nazwa_druzyny, rozegrane_mecze, bilans_bramek, zdobyte_punkty)
             VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, team_data)
    conn.commit()
    with open('sqlitecheck.txt', 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - Dodano nową drużynę o ID {cur.lastrowid}\n")
    return cur.lastrowid

def add_top_scorer(conn, top_scorer_data):
    sql = '''INSERT INTO top_scorers(miejsce, imie_nazwisko, pozycja, narodowosc, klub, liczba_strzelonych_bramek)
             VALUES(?,?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, top_scorer_data)
    conn.commit()
    with open('sqlitecheck.txt', 'a') as log_file:
        log_file.write(f"{datetime.datetime.now()} - Dodano nowego najlepszego strzelca o ID {cur.lastrowid}\n")
    return cur.lastrowid

def display_teams_with_positive_goal_difference(conn):
    query = "SELECT * FROM premier_league WHERE bilans_bramek > 0;"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Drużyny z dodatnim bilansem bramek:")
    for row in rows:
        print(row)

def display_arsenal_top_scorers(conn):
    query = "SELECT * FROM top_scorers WHERE klub = 'Arsenal';"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Najlepsi strzelcy Arsenalu:")
    for row in rows:
        print(row)

def display_midfielders_in_top_scorers(conn):
    query = "SELECT * FROM top_scorers WHERE pozycja = 'Pomocnik';"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Pomocnicy w tabeli najlepszych strzelców:")
    for row in rows:
        print(row)

def display_teams_starting_with_A(conn):
    query = "SELECT * FROM premier_league WHERE nazwa_druzyny LIKE 'A%';"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Drużyny zaczynające się na literę 'A':")
    for row in rows:
        print(row)

def display_top_scorers(conn):
    query = "SELECT * FROM top_scorers where liczba_strzelonych_bramek > 20;"
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    print("Najlepsi strzelcy z bramkami powyżej 20:")
    for row in rows:
        print(row)

if __name__ == "__main__":
    conn = create_connection("football_database.db")
    if conn is not None:
        delete_and_reset_tables(conn)
        execute_sql(conn, "CREATE TABLE IF NOT EXISTS premier_league (id INTEGER PRIMARY KEY, miejsce INTEGER, nazwa_druzyny TEXT, rozegrane_mecze INTEGER, bilans_bramek INTEGER, zdobyte_punkty INTEGER);", "Tworzenie tabeli premier_league")
        execute_sql(conn, "CREATE TABLE IF NOT EXISTS top_scorers (id INTEGER PRIMARY KEY, miejsce INTEGER, imie_nazwisko TEXT, pozycja TEXT, narodowosc TEXT, klub TEXT, liczba_strzelonych_bramek INTEGER);", "Tworzenie tabeli top_scorers")

        premier_league_data = [
            (1, "Arsenal", 38, 47, 90),
            (2, "Chelsea", 38, 37, 79),
            (3, "Manchester United", 38, 29, 75),
            (4, "Liverpool", 38, 18, 60),
            (5, "Newcastle United", 38, 12, 56),
            (6, "Aston Villa", 38, 4, 56),
            (7, "Charlton Athletic", 38, 0, 53),
            (8, "Bolton Wanderers", 38, -8, 53),
            (9, "Fulham", 38, 6, 52),
            (10, "Birmingham City", 38, -5, 50),
            (11, "Middlesbrough", 38, -8, 48),
            (12, "Southampton", 38, -1, 47),
            (13, "Portsmouth", 38, -7, 45),
            (14, "Tottenham Hotspur", 38, -10, 45),
            (15, "Blackburn Rovers", 38, -8, 44),
            (16, "Manchester City", 38, 1, 41),
            (17, "Everton", 38, -12, 39),
            (18, "Leicester City", 38, -17, 33),
            (19, "Leeds United", 38, -39, 33),
            (20, "Wolverhampton Wanderers", 38, -39, 33),
        ]

        top_scorers_data = [
            (1, "Thierry Henry", "Napastnik", "Francja", "Arsenal", 30),
            (2, "Alan Shearer", "Napastnik", "Anglia", "Newcastle United", 22),
            (3, "Louis Saha", "Napastnik", "Francja", "Manchester United", 20),
            (4, "Ruud van Nistelrooy", "Napastnik", "Holandia", "Manchester United", 20),
            (5, "Mikael Forssell", "Napastnik", "Finlandia", "Birmingham City", 17),
            (6, "Nicolas Anelka", "Napastnik", "Francja", "Manchester City", 17),
            (7, "Juan Pablo Ángel", "Napastnik", "Kolumbia", "Aston Villa", 16),
            (8, "Michael Owen", "Napastnik", "Anglia", "Liverpool", 16),
            (9, "Yakubu Aiyegbeni", "Napastnik", "Nigeria", "Portsmouth", 16),
            (10, "James Beattie", "Napastnik", "Anglia", "Southampton", 14),
            (11, "Robbie Keane", "Napastnik", "Irlandia", "Tottenham Hotspur", 14),
            (12, "Robert Pirès", "Pomocnik", "Francja", "Arsenal", 14),
            (13, "Jimmy Floyd Hasselbaink", "Napastnik", "Holandia", "Chelsea", 13),
            (14, "Kevin Phillips", "Napastnik", "Anglia", "Southampton", 13),
            (15, "Les Ferdinand", "Napastnik", "Anglia", "Leicester City", 12),
            (16, "Andrew Cole", "Napastnik", "Anglia", "Blackburn Rovers", 11),
            (17, "Mark Viduka", "Napastnik", "Australia", "Leeds United", 11),
            (18, "Paul Dickov", "Napastnik", "Szkocja", "Leicester City", 11),
            (19, "Frank Lampard", "Pomocnik", "Anglia", "Chelsea", 10),
            (20, "Jason Euell", "Pomocnik", "Anglia", "Charlton Athletic", 10),
            (21, "Hernán Crespo", "Napastnik", "Argentyna", "Chelsea", 10),
        ]

        for team_data in premier_league_data:
            team_id = add_team(conn, team_data)

        for top_scorer_data in top_scorers_data:
            top_scorer_id = add_top_scorer(conn, top_scorer_data)

        display_teams_with_positive_goal_difference(conn)

        display_arsenal_top_scorers(conn)

        display_midfielders_in_top_scorers(conn)

        display_teams_starting_with_A(conn)

        display_top_scorers(conn)

        conn.commit()
        conn.close()
        print("Zamknięto połączenie z bazą danych")
