import sqlite3
import os 
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets

# Ottieni il percorso dello script Python corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso completo al tuo database
database_path = os.path.join(script_directory, '../my_database.db')

conn = sqlite3.connect(database_path)  # Sostituisci 'database.db' con il nome del tuo file di database SQLite.

cursor = conn.cursor()
cursor.execute("SELECT * FROM presenze")
presenze_tot = cursor.fetchall()

df_presenze = pd.DataFrame(presenze_tot, columns=['id_presenze', 'dati', 'id_regione', 'id_anno', 'settore' ]) 

print(df_presenze)

cursor.execute("SELECT * FROM arrivi")
arrivi_tot = cursor.fetchall()

df_arrivi = pd.DataFrame(arrivi_tot, columns=['id_arrivi', 'dati', 'id_regione', 'id_anno', 'settore' ]) 

print(df_arrivi)

conn.close()

print(df_presenze.describe())
print(df_arrivi.describe())

# Creazione di un istogramma
plt.hist(df_presenze['dati'], bins=20)  # Esempio: visualizza l'istogramma dei dati

# Aggiungi etichette e titoli
plt.xlabel('Dati')
plt.ylabel('Frequenza')
plt.title('Istogramma dei dati di presenze')

# Mostra il grafico
plt.show()

# Visualizza alcune righe dei dati
print(df_presenze.head())

# Verifica se ci sono dati mancanti
missing_data = df_presenze.isnull().sum()
print("Dati mancanti:\n", missing_data)

# Istogramma delle presenze
plt.figure(figsize=(8, 6))
plt.hist(df_presenze['dati'], bins=20)
plt.title('Distribuzione delle presenze')
plt.xlabel('Presenze')
plt.ylabel('Frequenza')
plt.show()

# Box plot delle presenze
plt.figure(figsize=(8, 6))
plt.boxplot(df_presenze['dati'])
plt.title('Box Plot delle presenze')
plt.ylabel('Presenze')
plt.show()

# Seleziona solo le colonne numeriche
df_presenze_numeric = df_presenze.select_dtypes(include=['number'])

# Calcola la matrice di correlazione
correlation_matrix = df_presenze_numeric.corr()

# Visualizza la matrice di correlazione
print("Matrice di correlazione:\n", correlation_matrix)


# Visualizza un grafico a dispersione tra due variabili
plt.figure(figsize=(8, 6))
plt.scatter(df_presenze['id_regione'], df_presenze['dati'])
plt.title('Relazione tra regione e presenze')
plt.xlabel('Regione')
plt.ylabel('Presenze')
plt.show()

# Segmentazione dei dati per settore
settori = df_presenze['settore'].unique()
for settore in settori:
    subset = df_presenze[df_presenze['settore'] == settore]
    print(f"Statistiche per il settore {settore}:\n", subset.describe())
 
 
 
   