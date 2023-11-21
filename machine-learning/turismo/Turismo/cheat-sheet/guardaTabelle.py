  
import sqlite3

# Crea una connessione al database SQLite
conn = sqlite3.connect('turismo/my_database.db')

# Crea un cursore
cursor = conn.cursor()

# Esegui una query per ottenere una lista di tutte le tabelle nel database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Stampa i nomi delle tabelle
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")

    # Ottieni le informazioni sulla struttura della tabella
    cursor.execute(f"PRAGMA table_info({table_name});")
    table_info = cursor.fetchall()

    # Stampa le informazioni sulla struttura della tabella (nomi delle colonne)
    for column in table_info:
        column_name = column[1]
        print(f"  Column: {column_name}")

# Chiudi il cursore e la connessione
cursor.close()
conn.close()
