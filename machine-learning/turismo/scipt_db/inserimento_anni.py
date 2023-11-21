import sqlite3
import pandas as pd

conn = sqlite3.connect('../my_database.db')

cursor = conn.cursor ()


'''
cancello i dati nella tabella
cursor.execute('DELETE FROM anni;')
conn.commit()
cursor.close()
conn.close()
'''

#allora manca anno 2012 fixalo combiando la table e metti quella con 2012

table = "Arrivi_negli_alberghi_in_Italia_per_regione"

# Estrai gli anni distinti dai dati
distinct_years = pd.read_sql_query(f"SELECT DISTINCT Anno FROM {table}", conn)
distinct_years = distinct_years.rename(columns={'Anno': 'anno'})

# Inserisci i nuovi dati nella tabella 'anni'
distinct_years.to_sql('anni', conn, if_exists='append', index=False)

# Fetch e stampa i dati dalla tabella 'anni'
cursor.execute("SELECT * FROM anni")
rows = cursor.fetchall()

# Chiudi il cursore
cursor.close()

# Stampa i risultati
for row in rows:
    print(row)

# Chiudi la connessione al database
conn.close()