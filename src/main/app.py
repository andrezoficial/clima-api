from flask import Flask, jsonify, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Ruta principal
@app.route("/")
def home():
    return """
    <h1>API del Clima</h1>
    <p>Usa la ruta <code>/clima?ciudad=NombreCiudad</code> para consultar el tiempo.</p>
    """

# Ruta del clima
@app.route("/clima", methods=["GET"])
def obtener_clima():
    ciudad = request.args.get("ciudad", "Bogota")
    
    if not API_KEY:
        return jsonify({"error": "API Key no configurada"}), 500

    params = {
        "q": ciudad,
        "appid": API_KEY,
        "units": "metric",
        "lang": "es"
    }

    try:
        respuesta = requests.get(BASE_URL, params=params)
        respuesta.raise_for_status()
        datos = respuesta.json()

        clima = {
            "ciudad": datos["name"],
            "temperatura": datos["main"]["temp"],
            "humedad": datos["main"]["humidity"],
            "clima": datos["weather"][0]["description"]
        }
        return jsonify(clima), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 502

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)  

from flask_cors import CORS
CORS(app)  # Permite peticiones desde tu portfolio
