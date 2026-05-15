import json
import requests
from django.shortcuts import render
from django.conf import settings
from pathlib import Path
from tensorflow.keras.models import load_model


# =========================
# LOCAL MODEL LOAD (SAFE)
# =========================
MODEL_PATH = Path(settings.BASE_DIR) / "model.h5"

try:
    model = load_model(MODEL_PATH)
except Exception as e:
    model = None
    print("Model loading failed:", e)


# =========================
# IBM CONFIG (KEEP YOUR VALUES)
# =========================
API_KEY = "9XckV8KzTPcLUX-OTmq3OqJsI6LC94YN-VXVcaTL-QPo"

DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/019e208a-de12-70b2-8164-86fb2e51e43d/predictions?version=2021-05-01"



# =========================
# VIEW
# =========================
def home(request):

    prediction = None
    chart_data = []
    input_values = {}

    if request.method == "POST":

        try:
            # -------------------------
            # INPUTS
            # -------------------------
            N = float(request.POST.get("N", 0))
            P = float(request.POST.get("P", 0))
            K = float(request.POST.get("K", 0))
            temperature = float(request.POST.get("temperature", 0))
            humidity = float(request.POST.get("humidity", 0))
            ph = float(request.POST.get("ph", 0))
            rainfall = float(request.POST.get("rainfall", 0))

            input_values = {
                "N": N,
                "P": P,
                "K": K,
                "Temperature": temperature,
                "Humidity": humidity,
                "pH": ph,
                "Rainfall": rainfall
            }

            # -------------------------
            # IBM TOKEN
            # -------------------------
            token_response = requests.post(
                "https://iam.cloud.ibm.com/identity/token",
                data={
                    "apikey": API_KEY,
                    "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
                }
            )

            token_json = token_response.json()

            if "access_token" not in token_json:
                raise Exception("IBM token generation failed")

            mltoken = token_json["access_token"]

            # -------------------------
            # PAYLOAD
            # -------------------------
            payload_scoring = {
                "input_data": [
                    {
                        "fields": [
                            "N", "P", "K",
                            "temperature", "humidity", "ph", "rainfall"
                        ],
                        "values": [[
                            N, P, K,
                            temperature, humidity, ph, rainfall
                        ]]
                    }
                ]
            }

            # -------------------------
            # PREDICTION REQUEST
            # -------------------------
            response_scoring = requests.post(
                DEPLOYMENT_URL,
                json=payload_scoring,
                headers={
                    "Authorization": "Bearer " + mltoken,
                    "Content-Type": "application/json"
                }
            )

            result = response_scoring.json()
            print(result)

            prediction = result["predictions"][0]["values"][0][0]

            chart_data = [
                N, P, K,
                temperature, humidity, ph, rainfall
            ]

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render(request, "index.html", {
        "prediction": prediction,
        "chart_data": json.dumps(chart_data),
        "input_values": input_values
    })


















































































































































































API_KEY = "9XckV8KzTPcLUX-OTmq3OqJsI6LC94YN-VXVcaTL-QPo"

DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/019e208a-de12-70b2-8164-86fb2e51e43d/predictions?version=2021-05-01"

