from flask import Flask, render_template, request
import openrouteservice
import os

app = Flask(__name__)

# Substitua pela sua chave da OpenRouteService
API_KEY = os.environ.get("ORS_API_KEY")
# API_KEY = "5b3ce3597851110001cf62480221203250a14f1aba591f98da54de79"
cliente = openrouteservice.Client(key=API_KEY)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        origem = request.form["origem"]
        destino = request.form["destino"]
        try:
            coord_origem = cliente.pelias_search(text=origem)['features'][0]['geometry']['coordinates']
            coord_destino = cliente.pelias_search(text=destino)['features'][0]['geometry']['coordinates']

            coords = [coord_origem, coord_destino]
            rota = cliente.directions(coords, profile='driving-car', format='geojson')
            
            distancia_km = rota['features'][0]['properties']['summary']['distance'] / 1000
            duracao_min = rota['features'][0]['properties']['summary']['duration'] / 60

            resultado = {
                "origem": origem,
                "destino": destino,
                "distancia": f"{distancia_km:.2f} km",
                "duracao": f"{duracao_min:.0f} minutos"
            }
        except Exception as e:
            resultado = {"erro": "Erro ao calcular distância. Verifique as cidades e tente novamente."}

    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(debug=True)
