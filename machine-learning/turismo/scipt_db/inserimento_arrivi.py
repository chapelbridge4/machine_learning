import sqlite3
import os

# Ottieni il percorso del tuo script Python corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso completo al tuo database
database_path = os.path.join(script_directory, '../my_database.db')


# Crea una connessione al database SQLite
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

'''
#cancello i dati nella tabella
cursor.execute('DELETE FROM arrivi;')
conn.commit()
cursor.close()
conn.close()
'''

# Dizionari per mappare i nomi delle regioni e degli anni agli ID
region_name_to_id = {}
year_to_id = {}

# Esegui una query per selezionare i dati dalla tabella di origine
select_query_agriturismi = """
    SELECT Regione, Anno, Arrivi
    FROM Arrivi_negli_agriturismi_in_Italia_per_regione
"""

select_query_alberghiero = """
    SELECT Regione, Anno, Arrivi
    FROM Arrivi_negli_alberghi_in_Italia_per_regione
"""

select_query_campeggi = """
    SELECT Regione, Anno, Arrivi
    FROM Arrivi_nei_campeggi_in_Italia_per_regione
"""

# Recupera l'ID della regione per il nome della regione
cursor.execute("SELECT id_regione, nome_regione FROM regioni")
for row in cursor.fetchall():
    region_id, region_name = row
    region_name_to_id[region_name] = region_id

# Recupera l'ID dell'anno per l'anno
cursor.execute("SELECT id_anno, anno FROM anni")
for row in cursor.fetchall():
    year_id, year = row
    year_to_id[year] = year_id

# Esegui l'inserimento dei dati per ciascuna tabella di origine
for select_query, settore in [(select_query_agriturismi, 'agriturismo'), (select_query_alberghiero, 'alberghiero'), (select_query_campeggi, 'campeggio')]:
    cursor.execute(select_query)
    rows = cursor.fetchall()

    insert_query = """
        INSERT INTO arrivi (dati, id_regione, id_anno, settore)
        VALUES (?, ?, ?, ?)
    """

    for row in rows:
        regione, anno, arrivi = row
        region_id = region_name_to_id.get(regione)
        year_id = year_to_id.get(anno)

        if region_id is not None and year_id is not None:
            cursor.execute(insert_query, (arrivi, region_id, year_id, settore))

# Committo le modifiche nel database
conn.commit()

# Chiudi il cursore e la connessione al database
cursor.close()
conn.close()
