import pandas as pd
import sqlite3
import re  # Importa il modulo re per le espressioni regolari


# Elenco dei percorsi locali ai file CSV
file_paths = [
    'Negri-Davide-esameFinale/csv/winequality-red.csv',
    'Negri-Davide-esameFinale/csv/winequality-white.csv'
]

# Crea una connessione al database SQLite
conn = sqlite3.connect('Negri-Davide-esameFinale/database/db/wine.db')

file_len = len(file_paths) 


# Itera attraverso ciascun file e rinomina le tabelle dinamicamente
for i in range(file_len):
    try:
        file_path = file_paths[i] 
        # Leggi il file CSV nel DataFrame
        data = pd.read_csv(file_path, sep = ';')
        
        # Definisci un nuovo nome di tabella in base al nome del file
        table_name = f'table{i+1}'
        
        # Elimina la tabella esistente con il nuovo nome, se esiste
        drop_query = f"DROP TABLE IF EXISTS {table_name};"
        conn.execute(drop_query)
        
        # Aggiungi una colonna "wine_id" al DataFrame come colonna di indice
        data['wine_id'] = data.index.astype(int)
        
        # Rinomina le colonne sostituendo gli spazi con underscore
        data.columns = [re.sub(r'\s', '_', col) for col in data.columns]
        
        # Scrivi i dati nel database con il nuovo nome della tabella
        data.to_sql(table_name, conn, if_exists='replace', index=False,  dtype={'wine_id': 'INTEGER PRIMARY KEY AUTOINCREMENT'})
        
        # Stampa i nomi delle tabelle
        print(f"Table {table_name} created and loaded.")
    except Exception as e:
        print(f"Errore nel caricare il file {file_path}: {str(e)}")

# Definisci una convenzione di denominazione per i nuovi nomi delle tabelle
new_table_names = [
    'red_wine',
    'white_wine'
]

table_name_len = len(new_table_names)

# Rinomina le tabelle in base alla convenzione di denominazione
for f in range(table_name_len):
    try:
        new_table_name = new_table_names[f]
        # Definisci il nome attuale della tabella
        table_name = f'table{f+1}'
        
        # Verifica se la tabella attuale esiste prima di rinominarla
        check_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        cursor = conn.execute(check_query)
        if cursor.fetchone() is not None:
            # Elimina la tabella esistente con il nuovo nome, se esiste
            drop_query = f"DROP TABLE IF EXISTS {new_table_name};"
            conn.execute(drop_query)
        
            # Rinomina la tabella
            rename_query = f"ALTER TABLE {table_name} RENAME TO {new_table_name};"
            conn.execute(rename_query)
        
            # Stampa il nome della tabella dopo la rinominazione
            print(f"Table {table_name} renamed to {new_table_name}.")
        else:
            print(f"Table {table_name} does not exist.")
    except Exception as e:
        print(f"Errore nel rinominare la tabella {table_name}: {str(e)}")

# Close the database connection
#conn.close()


# Committo i cambiamenti nel db
conn.commit ()

rows = cursor.fetchall()

# Chiudi il cursore
cursor.close()

# Chiudi la connessione al database
conn.close()
