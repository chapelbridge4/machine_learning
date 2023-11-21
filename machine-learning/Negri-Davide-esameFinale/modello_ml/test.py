import requests

# Crea una richiesta POST
request = requests.post("http://127.0.0.1:8001/predict", json={
    "fixed_acidity": 7.8,
    "volatile_acidity": 0.4,
    "citric_acid": 0.6,
    "residual_sugar": 1.9,
    "chlorides": 0.09,
    "free_sulfur_dioxide": 11.0,
    "total_sulfur_dioxide": 42.0,
    "density": 0.9978,
    "pH": 3.21,
    "sulphates": 0.56,
    "alcohol": 12.5
})

# Controlla il codice di stato della risposta
if request.status_code == 200:
    # La predizione è avvenuta correttamente
    print(request.json())
else:
    # Si è verificato un errore
    print(request.status_code)