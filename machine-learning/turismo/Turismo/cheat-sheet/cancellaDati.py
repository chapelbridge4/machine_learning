import sqlite3

# Crea una connessione al database SQLite
conn = sqlite3.connect('turismo/my_database.db')
cursor = conn.cursor()

# Esegui l'istruzione SQL per cancellare tutti i dati dalla tabella "arrivi"
delete_query = "DELETE FROM arrivi"
cursor.execute(delete_query)

# Committo la cancellazione
conn.commit()

# Chiudi il cursore e la connessione al database
cursor.close()
conn.close()
