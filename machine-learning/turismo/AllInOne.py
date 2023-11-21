import pandas as pd
import sqlite3

'''
puoi estrapolare 4 tabelle 
'''
# Elenco dei percorsi locali ai file CSV
file_paths = [
    'turismo/Turismo/csvTurismo/Arrivi-negli-agriturismi-in-Italia-per-regione.csv',
    'turismo/Turismo/csvTurismo/Arrivi-negli-esercizi-alberghieri-in-Italia-per-regione.csv',
    'turismo/Turismo/csvTurismo/Arrivi-nei-campeggi-e-villaggi-turistici-in-italia-per-regione.csv',
    'turismo/Turismo/csvTurismo/Presenze-negli-agriturismi-in-Italia-per-regione.csv',
    'turismo/Turismo/csvTurismo/Presenze-negli-esercizi-alberghieri-in-Italia-per-regione.csv',
    'turismo/Turismo/csvTurismo/Presenze-nei-campeggi-e-villaggi-turistici-in-italia-per-regione.csv'
]

# Crea una connessione al database SQLite
conn = sqlite3.connect('turismo/my_database.db')

file_len = len(file_paths) 


# Iterate through each file and rename the tables dynamically
for i in range(file_len):
    try:
        file_path = file_paths[i] 
        # Leggi il file CSV nel DataFrame
        data = pd.read_csv(file_path, sep = ';')
        
        # Define a new table name based on the file name
        table_name = f'table{i+1}'
        
        # Drop the existing table with the new name if it exists
        drop_query = f"DROP TABLE IF EXISTS {table_name};"
        conn.execute(drop_query)
        
        # Write the data to the database with the new table name
        data.to_sql(table_name, conn, if_exists='replace')
        
        # Print the table name
        print(f"Table {table_name} created and loaded.")
    except Exception as e:
        print(f"Errore nel caricare il file {file_path}: {str(e)}")

# Define a naming convention for the new table names
new_table_names = [
    'Arrivi_negli_agriturismi_in_Italia_per_regione',
    'Arrivi_negli_alberghi_in_Italia_per_regione',
    'Arrivi_nei_campeggi_in_Italia_per_regione',
    'Presenze_negli_agriturismi_in_Italia_per_regione',
    'Presenze_negli_alberghi_in_Italia_per_regione',
    'Presenze_nei_campeggi_in_Italia_per_regione'
]

table_name_len = len(new_table_names)
# Rename the tables based on the naming convention
for f in range(table_name_len):
    try:
        new_table_name = new_table_names[f]
        # Define the current table name
        table_name = f'table{f+1}'
        
        # Check if the current table exists before renaming
        check_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        cursor = conn.execute(check_query)
        if cursor.fetchone() is not None:
            # Drop the existing table with the new name if it exists
            drop_query = f"DROP TABLE IF EXISTS {new_table_name};"
            conn.execute(drop_query)
        
            # Rename the table
            rename_query = f"ALTER TABLE {table_name} RENAME TO {new_table_name};"
            conn.execute(rename_query)
        
            # Print the table name after renaming
            print(f"Table {table_name} renamed to {new_table_name}.")
        else:
            print(f"Table {table_name} does not exist.")
    except Exception as e:
        print(f"Errore nel rinominare la tabella {table_name}: {str(e)}")

# Close the database connection
#conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    conn = sqlite3.connect ( 'my_database.db' )

    cursor = conn.cursor ()

    cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS regioni (
        id_regione INTEGER PRIMARY KEY,
        nome_regione TEXT
    )
    """)

    cursor.execute ( """
    CREATE TABLE IF NOT EXISTS anni (
        id_anno INTEGER PRIMARY KEY,
        anno INTEGER UNIQUE
    )
    """ )

    cursor.execute ( """
    CREATE TABLE IF NOT EXISTS arrivi (
        id_arrivi INTEGER PRIMARY KEY,
        dati INTEGER,
        id_regione INTEGER,
        id_anno INTEGER,
        FOREIGN KEY(id_regione) REFERENCES regioni(id_regione),
        FOREIGN KEY(id_anno) REFERENCES anni(id_anno)
    )
    """ )

    cursor.execute ( """
    CREATE TABLE IF NOT EXISTS presenze (
        id_presenze INTEGER PRIMARY KEY,
        dati INTEGER,
        id_regione INTEGER,
        id_anno INTEGER,
        FOREIGN KEY(id_regione) REFERENCES regioni(id_regione),
        FOREIGN KEY(id_anno) REFERENCES anni(id_anno)
    )
    """ )
    
    # Aggiungi una colonna 'settore' alle tabelle 'arrivi' e 'presenze'
    cursor.execute("ALTER TABLE arrivi ADD COLUMN settore TEXT;")
    cursor.execute("ALTER TABLE presenze ADD COLUMN settore TEXT;")

    
    # Committo i cambiamenti nel db
    conn.commit ()

table = "Arrivi_negli_agriturismi_in_Italia_per_regione"

tables_arrivi = ['Arrivi_negli_agriturismi_in_Italia_per_regione',
    'Arrivi_negli_alberghi_in_Italia_per_regione',
    'Arrivi_nei_campeggi_in_Italia_per_regione']

tables_presenze = ['Presenze_negli_agriturismi_in_Italia_per_regione',
    'Presenze_negli_alberghi_in_Italia_per_regione',
    'Presenze_nei_campeggi_in_Italia_per_regione']

'''
# Estrai gli anni distinti dai dati
distinct_years = pd.read_sql_query(f"SELECT DISTINCT Anno FROM {table}", conn)
distinct_years = distinct_years.rename(columns={'Anno': 'anno'})

# Inserisci i nuovi dati nella tabella 'anni'
distinct_years.to_sql('anni', conn, if_exists='append', index=False)

# Estrai le regioni distinte dai dati
distinct_region = pd.read_sql_query(f"SELECT DISTINCT Regione FROM {table}", conn)
distinct_region = distinct_region.rename(columns={'Regione': 'nome_regione'})

# Inserisci i nuovi dati nella tabella 'anni'
distinct_region.to_sql('regioni', conn, if_exists='append', index=False)

# Fetch e stampa i dati dalla tabella 'anni'
#cursor.execute("SELECT * FROM anni")
cursor.execute("SELECT * FROM regioni")
'''



rows = cursor.fetchall()

# Chiudi il cursore
cursor.close()

# Stampa i risultati
for row in rows:
    print(row)

# Chiudi la connessione al database
conn.close()