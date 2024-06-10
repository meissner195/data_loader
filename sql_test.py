import sqlite3
import os

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('example.db')    

cursor = conn.cursor()
cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users';''')
if cursor.fetchone()[0] == 1:
    # Tabelle existiert, Spalten überprüfen
    cursor.execute('''PRAGMA table_info(users);''')
    columns = cursor.fetchall()
    column_names = [col[1] for col in columns]
    print("Tabelle existiert mit folgenden Spalten: ", column_names)
else:
    print("Die Tabelle 'users' existiert nicht")
    # Tabelle erstellen
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    '''
    cursor.execute(create_table_query)
    conn.commit()

# Daten einfügen
insert_query = '''
INSERT INTO users (name, age, email)
VALUES (?, ?, ?)
'''
data_to_check = [("Alice", 30, "alice@example.com"), 
                 ("Bob", 25, "bob@example.com"), 
                 ("Ruben", 26, "ruben@example.com"), 
                 ("Klaus", 54, "klaus@example.com"),
                 ("Florian", 28, "florian@example.com")]

for data in data_to_check:
    email = data[2]
    cursor.execute("SELECT COUNT(*) FROM users WHERE email=?", (email,))
    result = cursor.fetchone()[0]
    if not result:
        cursor.execute(insert_query, data)
        conn.commit()

# Daten lesen
select_query = '''
SELECT name, age, email
FROM users
ORDER BY age ASC
'''
cursor.execute(select_query)
rows = cursor.fetchall()
for row in rows:
    print(row)

# Daten aktualisieren
update_query = '''
UPDATE users
SET age = ?
WHERE name = ?
'''
cursor.execute(update_query, (31, "Alice"))
conn.commit()

# Daten löschen
delete_query = '''
DELETE FROM users
WHERE name = ?
'''
cursor.execute(delete_query, ("Bob",))
conn.commit()

# Verbindung schließen
conn.close()
