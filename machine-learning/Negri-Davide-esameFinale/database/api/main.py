from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import os
#uvicorn main:app --reload

#funziona tutto, creazione di fast api per operazioni CRUD

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
# Ottieni il percorso dello script Python corrente
script_directory = os.path.dirname(os.path.abspath(__file__))

# Costruisci il percorso completo al tuo database
database_path = os.path.join(script_directory, '../db/wine.db')    
    
class White_wine(BaseModel):
    fixed_acidity: float 
    volatile_acidity: float 
    citric_acid: float 
    residual_sugar: float 
    chlorides: float
    free_sulfur_dioxide: float 
    total_sulfur_dioxide: float 
    density: float 
    ph: float 
    sulphates: float 
    alcohol: float 
    quality: int 
    wine_id: int

    
@app.get("/white_wine/{wine_id}", response_model=White_wine)
def get_white_wine(wine_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Esegui una query per recuperare i dati del vino bianco
    cursor.execute("SELECT * FROM white_wine WHERE wine_id=?", (wine_id,))
    white_wine_data = cursor.fetchone()

    conn.close()

    if white_wine_data is not None:
        # Effettua una conversione esplicita di wine_id a int, wine_id posizione [12] perchè 
        # avendo inserito la colonna dopo aver caricato i csv è stata spostata in fondo
        wine_id = int(white_wine_data[12])
        return {
            "wine_id": wine_id,
            "fixed_acidity": white_wine_data[0],
            "volatile_acidity": white_wine_data[1],
            "citric_acid": white_wine_data[2],
            "residual_sugar": white_wine_data[3],
            "chlorides": white_wine_data[4],
            "free_sulfur_dioxide": white_wine_data[5],
            "total_sulfur_dioxide": white_wine_data[6],
            "density": white_wine_data[7],
            "ph": white_wine_data[8],
            "sulphates": white_wine_data[9],
            "alcohol": white_wine_data[10],
            "quality": white_wine_data[11]
        }
    else:
        raise HTTPException(status_code=404, detail="Vino bianco non trovato")

@app.post("/white_wine", response_model=White_wine)
def create_white_wine(white_wine: White_wine):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Inserisci un nuovo vino bianco nel database
    cursor.execute("""
        INSERT INTO white_wine 
        (fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
         free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, quality)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        white_wine.fixed_acidity, white_wine.volatile_acidity, white_wine.citric_acid,
        white_wine.residual_sugar, white_wine.chlorides, white_wine.free_sulfur_dioxide,
        white_wine.total_sulfur_dioxide, white_wine.density, white_wine.ph,
        white_wine.sulphates, white_wine.alcohol, white_wine.quality
    ))
    
    # Ottieni l'ID del nuovo vino bianco
    wine_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return {**white_wine.model_dump(), "wine_id": wine_id}


@app.put("/white_wine/{wine_id}", response_model=White_wine)
def update_white_wine(wine_id: int, white_wine: White_wine):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se il vino bianco con l'ID specificato esiste nel database
    cursor.execute("SELECT * FROM white_wine WHERE wine_id=?", (wine_id,))
    existing_white_wine = cursor.fetchone()

    if existing_white_wine is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Vino bianco non trovato")

    # Esegui l'aggiornamento dei dati del vino bianco nel database
    update_query = """
        UPDATE white_wine SET
        fixed_acidity=?, volatile_acidity=?, citric_acid=?, residual_sugar=?,
        chlorides=?, free_sulfur_dioxide=?, total_sulfur_dioxide=?, density=?,
        ph=?, sulphates=?, alcohol=?, quality=?
        WHERE wine_id=?
    """
    cursor.execute(update_query, (
        white_wine.fixed_acidity, white_wine.volatile_acidity, white_wine.citric_acid,
        white_wine.residual_sugar, white_wine.chlorides, white_wine.free_sulfur_dioxide,
        white_wine.total_sulfur_dioxide, white_wine.density, white_wine.ph,
        white_wine.sulphates, white_wine.alcohol, white_wine.quality, wine_id
    ))

    conn.commit()

    conn.close()

    # Restituisci i dati aggiornati del vino bianco
    return {**white_wine.model_dump(), "wine_id": wine_id}

@app.delete("/white_wine/{wine_id}")
def delete_white_wine(wine_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se il vino bianco con l'ID specificato esiste nel database
    cursor.execute("SELECT * FROM white_wine WHERE wine_id=?", (wine_id,))
    existing_white_wine = cursor.fetchone()

    if existing_white_wine is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Vino bianco non trovato")

    # Esegui la query di eliminazione
    delete_query = "DELETE FROM white_wine WHERE wine_id=?"
    cursor.execute(delete_query, (wine_id,))

    conn.commit()
    conn.close()

    return {"message": f"Vino bianco con ID {wine_id} eliminato con successo"}



class Red_wine(BaseModel):
    fixed_acidity: float 
    volatile_acidity: float 
    citric_acid: float 
    residual_sugar: float 
    chlorides: float
    free_sulfur_dioxide: float 
    total_sulfur_dioxide: float 
    density: float 
    ph: float 
    sulphates: float 
    alcohol: float 
    quality: int 
    wine_id: int

@app.get("/red_wine/{wine_id}", response_model=Red_wine)
def get_red_wine(wine_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Esegui una query per recuperare i dati del vino rosso
    cursor.execute("SELECT * FROM red_wine WHERE wine_id=?", (wine_id,))
    red_wine_data = cursor.fetchone()

    conn.close()

    if red_wine_data is not None:
        # Effettua una conversione esplicita di wine_id a int
        wine_id = int(red_wine_data[12])
        return {
            "wine_id": wine_id,
            "fixed_acidity": red_wine_data[0],
            "volatile_acidity": red_wine_data[1],
            "citric_acid": red_wine_data[2],
            "residual_sugar": red_wine_data[3],
            "chlorides": red_wine_data[4],
            "free_sulfur_dioxide": red_wine_data[5],
            "total_sulfur_dioxide": red_wine_data[6],
            "density": red_wine_data[7],
            "ph": red_wine_data[8],
            "sulphates": red_wine_data[9],
            "alcohol": red_wine_data[10],
            "quality": red_wine_data[11]
        }
    else:
        raise HTTPException(status_code=404, detail="vino rosso non trovato")

@app.post("/red_wine", response_model=Red_wine)
def create_red_wine(red_wine: Red_wine):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Inserisci un nuovo vino rosso nel database
    cursor.execute("""
        INSERT INTO red_wine 
        (fixed_acidity, volatile_acidity, citric_acid, residual_sugar, chlorides,
         free_sulfur_dioxide, total_sulfur_dioxide, density, ph, sulphates, alcohol, quality)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        red_wine.fixed_acidity, red_wine.volatile_acidity, red_wine.citric_acid,
        red_wine.residual_sugar, red_wine.chlorides, red_wine.free_sulfur_dioxide,
        red_wine.total_sulfur_dioxide, red_wine.density, red_wine.ph,
        red_wine.sulphates, red_wine.alcohol, red_wine.quality
    ))
    
    # Ottieni l'ID del nuovo vino rosso
    wine_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    return {**red_wine.model_dump(), "wine_id": wine_id}


@app.put("/red_wine/{wine_id}", response_model=Red_wine)
def update_red_wine(wine_id: int, red_wine: Red_wine):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se il vino rosso con l'ID specificato esiste nel database
    cursor.execute("SELECT * FROM red_wine WHERE wine_id=?", (wine_id,))
    existing_red_wine = cursor.fetchone()

    if existing_red_wine is None:
        conn.close()
        raise HTTPException(status_code=404, detail="vino rosso non trovato")

    # Esegui l'aggiornamento dei dati del vino rosso nel database
    update_query = """
        UPDATE red_wine SET
        fixed_acidity=?, volatile_acidity=?, citric_acid=?, residual_sugar=?,
        chlorides=?, free_sulfur_dioxide=?, total_sulfur_dioxide=?, density=?,
        ph=?, sulphates=?, alcohol=?, quality=?
        WHERE wine_id=?
    """
    cursor.execute(update_query, (
        red_wine.fixed_acidity, red_wine.volatile_acidity, red_wine.citric_acid,
        red_wine.residual_sugar, red_wine.chlorides, red_wine.free_sulfur_dioxide,
        red_wine.total_sulfur_dioxide, red_wine.density, red_wine.ph,
        red_wine.sulphates, red_wine.alcohol, red_wine.quality, wine_id
    ))

    conn.commit()

    conn.close()

    # Restituisci i dati aggiornati del vino rosso
    return {**red_wine.model_dump(), "wine_id": wine_id}

@app.delete("/red_wine/{wine_id}")
def delete_red_wine(wine_id: int):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Verifica se il vino rosso con l'ID specificato esiste nel database
    cursor.execute("SELECT * FROM red_wine WHERE wine_id=?", (wine_id,))
    existing_red_wine = cursor.fetchone()

    if existing_red_wine is None:
        conn.close()
        raise HTTPException(status_code=404, detail="vino rosso non trovato")

    # Esegui la query di eliminazione
    delete_query = "DELETE FROM red_wine WHERE wine_id=?"
    cursor.execute(delete_query, (wine_id,))

    conn.commit()
    conn.close()

    return {"message": f"vino rosso con ID {wine_id} eliminato con successo"}