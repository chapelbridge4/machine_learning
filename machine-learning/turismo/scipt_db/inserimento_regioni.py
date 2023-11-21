import sqlite3
import pandas as pd
import os 

# Ottieni il percorso del tuo script Python corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso completo al tuo database
database_path = os.path.join(script_directory, '../my_database.db')

conn = sqlite3.connect(database_path)


cursor = conn.cursor ()

table = "Arrivi_negli_agriturismi_in_Italia_per_regione"


# Estrai le regioni distinte dai dati
distinct_region = pd.read_sql_query(f"SELECT DISTINCT Regione FROM {table}", conn)
distinct_region = distinct_region.rename(columns={'Regione': 'nome_regione'})

# Inserisci i nuovi dati nella tabella 'anni'
distinct_region.to_sql('regioni', conn, if_exists='append', index=False)

# Fetch e stampa i dati dalla tabella 'anni'
cursor.execute("SELECT * FROM regioni")
rows = cursor.fetchall()

# Chiudi il cursore
cursor.close()

# Stampa i risultati
for row in rows:
    print(row)

# Chiudi la connessione al database
conn.close()