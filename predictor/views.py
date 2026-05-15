from django.shortcuts import render
import requests
import json

API_KEY = "9XckV8KzTPcLUX-OTmq3OqJsI6LC94YN-VXVcaTL-QPo"

DEPLOYMENT_URL = "https://au-syd.ml.cloud.ibm.com/ml/v4/deployments/019e208a-de12-70b2-8164-86fb2e51e43d/predictions?version=2021-05-01"


def home(request):

    prediction = None
    chart_data = []
    input_values = {}

    if request.method == "POST":

        try:

            N = float(request.POST.get("N"))
            P = float(request.POST.get("P"))
            K = float(request.POST.get("K"))
            temperature = float(request.POST.get("temperature"))
            humidity = float(request.POST.get("humidity"))
            ph = float(request.POST.get("ph"))
            rainfall = float(request.POST.get("rainfall"))

            input_values = {
                'N': N,
                'P': P,
                'K': K,
                'Temperature': temperature,
                'Humidity': humidity,
                'pH': ph,
                'Rainfall': rainfall
            }

            # Generate Token
            token_response = requests.post(
                'https://iam.cloud.ibm.com/identity/token',
                data={
                    "apikey": API_KEY,
                    "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'
                }
            )

            mltoken = token_response.json()["access_token"]

            # Payload
            payload_scoring = {
                "input_data": [
                    {
                        "fields": [
                            "N",
                            "P",
                            "K",
                            "temperature",
                            "humidity",
                            "ph",
                            "rainfall"
                        ],
                        "values": [[
                            N,
                            P,
                            K,
                            temperature,
                            humidity,
                            ph,
                            rainfall
                        ]]
                    }
                ]
            }

            # Prediction Request
            response_scoring = requests.post(
                DEPLOYMENT_URL,
                json=payload_scoring,
                headers={
                    'Authorization': 'Bearer ' + mltoken,
                    'Content-Type': 'application/json'
                }
            )

            result = response_scoring.json()

            print(result)

            prediction = result['predictions'][0]['values'][0][0]

            chart_data = [
                N,
                P,
                K,
                temperature,
                humidity,
                ph,
                rainfall
            ]

        except Exception as e:
            prediction = f"Error: {str(e)}"

    # IMPORTANT
    return render(request, 'index.html', {
        'prediction': prediction,
        'chart_data': json.dumps(chart_data),
        'input_values': input_values
    })