import fastapi
from pypmml import Model
import uvicorn
import json

# Importo il modello PMML
model = Model.fromFile('Negri-Davide-esameFinale/modello_ml/modello/wines_true.pmml')

# Creo l'app FastAPI
app = fastapi.FastAPI()

# Creo la route per la predizione
@app.post("/predict")
def predict(data: dict):
    # Converto i dati in un dizionario di valori numerici
    input_features = {
        key: float(value)
        for key, value in data.items()
    }

    # Effettuo la predizione
    prediction = model.predict(input_features)

    # Restituisco la predizione in formato JSON
    return fastapi.responses.JSONResponse(content=json.dumps({"prediction": float(prediction['result'])}))

# Avvio l'app FastAPI
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
    

