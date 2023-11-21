import sqlite3

# Connetti al database SQLite
conn = sqlite3.connect('my_database.db')
cursor = conn.cursor()

# Esegui una query SQL per selezionare tutti i dati dalle tabelle

#cursor.execute("SELECT * FROM anni")

cursor.execute("SELECT * FROM regioni")

rows = cursor.fetchall()

# Stampa i risultati
for row in rows:
    print(row)

# Chiudi il cursore
cursor.close()

# Chiudi la connessione al database
conn.close()
