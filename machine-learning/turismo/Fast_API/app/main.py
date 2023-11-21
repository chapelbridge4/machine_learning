from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
#uvicorn main:app --reload

#api fatte concluse non toccare nulla 

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Importa i moduli per le operazioni CRUD relative a entità specifiche

# Ottieni il percorso dello script Python corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso completo al tuo database
database_path = os.path.join(script_directory, '../../my_database.db')

class Regione(BaseModel):
    id_regione: int
    nome_regione: str


# questa get va lasciala così, controlla solo sti percorsi del cacchio va tutto per regioni
@app.get("/regione/{regione_id}", response_model=Regione)
def get_regione(regione_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Esegui una query per recuperare i dati della regione
    cursor.execute("SELECT * FROM regioni WHERE id_regione=?", (regione_id,))
    regione = cursor.fetchone()

    conn.close()

    if regione is not None:
        return {"id_regione": regione[0], "nome_regione": regione[1]}
    else:
        raise HTTPException(status_code=404, detail="Regione non trovata")



@app.post("/crea_regione", response_model=Regione)
async def create_regione(regione: Regione):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Inserisci una nuova regione nel database
    cursor.execute("INSERT INTO regioni (nome_regione) VALUES (?)", (regione.nome_regione,))
    conn.commit()

    # Recupera l'ID della regione appena creata
    cursor.execute("SELECT last_insert_rowid()")
    new_region_id = cursor.fetchone()[0]

    conn.close()

    # Restituisci il risultato in modo asincrono
    return {"id_regione": new_region_id, "nome_regione": regione.nome_regione}


@app.put("/aggiorna_regione/{regione_id}", response_model=Regione)
async def update_regione(regione_id: int, updated_region: Regione):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se la regione esiste
    cursor.execute("SELECT id_regione, nome_regione FROM regioni WHERE id_regione=?", (regione_id,))
    existing_region = cursor.fetchone()

    if existing_region is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Regione non trovata")

    # Esegui l'aggiornamento dei dati nel database
    cursor.execute("UPDATE regioni SET nome_regione = ? WHERE id_regione = ?", (updated_region.nome_regione, regione_id))
    conn.commit()

    # Chiudi la connessione al database
    conn.close()

    # Restituisci i dati aggiornati
    return {"id_regione": regione_id, "nome_regione": updated_region.nome_regione}

@app.delete("/elimina_regione", response_model=Regione)
async def delete_regione(regione: Regione):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se la regione esiste
    cursor.execute("SELECT id_regione, nome_regione FROM regioni WHERE id_regione=?", (regione.id_regione,))
    existing_region = cursor.fetchone()

    if existing_region is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Regione non trovata")

    # Esegui l'eliminazione dei dati nel database
    regione_id = int(regione.id_regione)
    cursor.execute("DELETE FROM regioni WHERE id_regione = ?", (regione_id,))
    conn.commit()

    # Chiudi la connessione al database
    conn.close()

    # Restituisci i dati della regione eliminata
    return {"id_regione": existing_region[0], "nome_regione": existing_region[1]}



class Anni(BaseModel):
    id_anno: int
    anno: int
    
class Arrivi(BaseModel):
    id_arrivi: int
    dati: int
    id_regione: int
    id_anno: int
    settore: str

@app.get("/arrivi/{arrivi_id}", response_model=Arrivi)
def get_arrivi(arrivi_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Esegui una query per recuperare i dati di Arrivi
    cursor.execute("SELECT * FROM arrivi WHERE id_arrivi=?", (arrivi_id,))
    arrivi = cursor.fetchone()

    conn.close()

    if arrivi is not None:
        return {"id_arrivi": arrivi[0], "dati": arrivi[1], "id_regione": arrivi[2], "id_anno": arrivi[3], "settore": arrivi[4]}
    else:
        raise HTTPException(status_code=404, detail="Dati di Arrivi non trovati")

@app.post("/crea_arrivi", response_model=Arrivi)
async def create_arrivi(arrivi: Arrivi):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Inserisci nuovi dati di Arrivi nel database
    cursor.execute("INSERT INTO arrivi (dati, id_regione, id_anno, settore) VALUES (?, ?, ?, ?)",
                   (arrivi.dati, arrivi.id_regione, arrivi.id_anno, arrivi.settore))
    conn.commit()

    # Recupera l'ID dei dati di Arrivi appena creati
    cursor.execute("SELECT last_insert_rowid()")
    new_arrivi_id = cursor.fetchone()[0]

    conn.close()

    # Restituisci il risultato in modo asincrono
    return {"id_arrivi": new_arrivi_id, "dati": arrivi.dati, "id_regione": arrivi.id_regione, "id_anno": arrivi.id_anno, "settore": arrivi.settore}

@app.put("/aggiorna_arrivi/{arrivi_id}", response_model=Arrivi)
async def update_arrivi(arrivi_id: int, updated_arrivi: Arrivi):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se i dati di Arrivi esistono
    cursor.execute("SELECT id_arrivi, dati, id_regione, id_anno, settore FROM arrivi WHERE id_arrivi=?", (arrivi_id,))
    existing_arrivi = cursor.fetchone()

    if existing_arrivi is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Dati di Arrivi non trovati")

    # Esegui l'aggiornamento dei dati nel database
    cursor.execute("UPDATE arrivi SET dati = ?, id_regione = ?, id_anno = ?, settore = ? WHERE id_arrivi = ?",
                   (updated_arrivi.dati, updated_arrivi.id_regione, updated_arrivi.id_anno, updated_arrivi.settore, arrivi_id))
    conn.commit()

    conn.close()

    # Restituisci i dati aggiornati
    return {"id_arrivi": arrivi_id, "dati": updated_arrivi.dati, "id_regione": updated_arrivi.id_regione, "id_anno": updated_arrivi.id_anno, "settore": updated_arrivi.settore}

@app.delete("/elimina_arrivi/{arrivi_id}", response_model=Arrivi)
async def delete_arrivi(arrivi_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se i dati di Arrivi esistono
    cursor.execute("SELECT id_arrivi, dati, id_regione, id_anno, settore FROM arrivi WHERE id_arrivi=?", (arrivi_id,))
    existing_arrivi = cursor.fetchone()

    if existing_arrivi is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Dati di Arrivi non trovati")

    # Esegui l'eliminazione dei dati di Arrivi dal database
    cursor.execute("DELETE FROM arrivi WHERE id_arrivi = ?", (arrivi_id,))
    conn.commit()

    conn.close()

    # Restituisci i dati di Arrivi eliminati
    return {"id_arrivi": existing_arrivi[0], "dati": existing_arrivi[1], "id_regione": existing_arrivi[2], "id_anno": existing_arrivi[3], "settore": existing_arrivi[4]}


    
class Presenze(BaseModel):
    id_presenze: int
    dati: int
    id_regione: int
    id_anno: int
    settore: str

@app.get("/presenze/{presenze_id}", response_model=Presenze)
def get_presenze(presenze_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Esegui una query per recuperare i dati di Presenze
    cursor.execute("SELECT * FROM presenze WHERE id_presenze=?", (presenze_id,))
    presenze = cursor.fetchone()

    conn.close()

    if presenze is not None:
        return {"id_presenze": presenze[0], "dati": presenze[1], "id_regione": presenze[2], "id_anno": presenze[3], "settore": presenze[4]}
    else:
        raise HTTPException(status_code=404, detail="Dati di Presenze non trovati")

@app.post("/crea_presenze", response_model=Presenze)
async def create_presenze(presenze: Presenze):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Inserisci nuovi dati di Presenze nel database
    cursor.execute("INSERT INTO presenze (dati, id_regione, id_anno, settore) VALUES (?, ?, ?, ?)",
                   (presenze.dati, presenze.id_regione, presenze.id_anno, presenze.settore))
    conn.commit()

    # Recupera l'ID dei dati di Presenze appena creati
    cursor.execute("SELECT last_insert_rowid()")
    new_presenze_id = cursor.fetchone()[0]

    conn.close()

    # Restituisci il risultato in modo asincrono
    return {"id_presenze": new_presenze_id, "dati": presenze.dati, "id_regione": presenze.id_regione, "id_anno": presenze.id_anno, "settore": presenze.settore}

@app.put("/aggiorna_presenze/{presenze_id}", response_model=Presenze)
async def update_presenze(presenze_id: int, updated_presenze: Presenze):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se i dati di Presenze esistono
    cursor.execute("SELECT id_presenze, dati, id_regione, id_anno, settore FROM presenze WHERE id_presenze=?", (presenze_id,))
    existing_presenze = cursor.fetchone()

    if existing_presenze is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Dati di Presenze non trovati")

    # Esegui l'aggiornamento dei dati nel database
    cursor.execute("UPDATE presenze SET dati = ?, id_regione = ?, id_anno = ?, settore = ? WHERE id_presenze = ?",
                   (updated_presenze.dati, updated_presenze.id_regione, updated_presenze.id_anno, updated_presenze.settore, presenze_id))
    conn.commit()

    conn.close()

    # Restituisci i dati aggiornati
    return {"id_prsenze": presenze_id, "dati": updated_presenze.dati, "id_regione": updated_presenze.id_regione, "id_anno": updated_presenze.id_anno, "settore": updated_presenze.settore}

@app.delete("/elimina_presenze/{presenze_id}", response_model=Presenze)
async def delete_presenze(presenze_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se i dati di Presenze esistono
    cursor.execute("SELECT id_presenze, dati, id_regione, id_anno, settore FROM presenze WHERE id_presenze=?", (presenze_id,))
    existing_presenze = cursor.fetchone()

    if existing_presenze is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Dati di Presenze non trovati")

    # Esegui l'eliminazione dei dati di Presenze dal database
    cursor.execute("DELETE FROM presenze WHERE id_presenze = ?", (presenze_id,))
    conn.commit()

    conn.close()

    # Restituisci i dati di Presenze eliminati
    return {"id_presenze": existing_presenze[0], "dati": existing_presenze[1], "id_regione": existing_presenze[2], "id_anno": existing_presenze[3], "settore": existing_presenze[4]}
