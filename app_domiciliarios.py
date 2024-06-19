Python 3.12.4 (tags/v3.12.4:8e8a4ba, Jun  6 2024, 19:30:16) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
>>> from flask import Flask, request, jsonify
... from math import radians, cos, sin, sqrt, atan2
... 
... app = Flask(__name__)
... 
... # Simulando una base de datos
... domiciliarios = [
...     {
...         'id_Domiciliario': 1,
...         'Nombre': 'Carlos Sanchez',
...         'UbicacionDomiciliario': (4.60971, -74.08175),  # Latitud, Longitud
...         'Taria': 15.5,
...         'FotoDomiciliario': 'foto1.jpg',
...         'TipoVehiculo': 'Moto',
...         'EstrellasCalificacion': 4
...     },
...     {
...         'id_Domiciliario': 2,
...         'Nombre': 'Maria Perez',
...         'UbicacionDomiciliario': (4.61577, -74.07021),
...         'Taria': 10.0,
...         'FotoDomiciliario': 'foto2.jpg',
...         'TipoVehiculo': 'Bicicleta',
...         'EstrellasCalificacion': 5
...     },
...     {
...         'id_Domiciliario': 3,
...         'Nombre': 'Juan Lopez',
...         'UbicacionDomiciliario': (4.6000, -74.0833),
...         'Taria': 12.0,
...         'FotoDomiciliario': 'foto3.jpg',
...         'TipoVehiculo': 'Moto',
...         'EstrellasCalificacion': 3
...     },
...     # ... más domiciliarios
... ]
... 
def calcular_distancia(coord1, coord2):
    R = 6373.0  # radio de la Tierra en km

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c
    return distancia

@app.route('/domiciliarios/cercanos', methods=['POST'])
def obtener_domiciliarios_cercanos():
    data = request.get_json()
    ubicacion_establecimiento = data['UbicacionEstablecimiento']
    
    domiciliarios_ordenados = sorted(domiciliarios, key=lambda x: calcular_distancia(x['UbicacionDomiciliario'], ubicacion_establecimiento))
    tres_cercanos = domiciliarios_ordenados[:3]
    
    for d in tres_cercanos:
        d['ImagenAsignacion'] = d['FotoDomiciliario']  # Aquí podrías generar una imagen con la asignación
    
    return jsonify(tres_cercanos), 200

@app.route('/domiciliarios/tipo_vehiculo/<tipo>', methods=['GET'])
def obtener_domiciliarios_por_tipo_vehiculo(tipo):
    resultado = [d for d in domiciliarios if d['TipoVehiculo'].lower() == tipo.lower()]
    return jsonify(resultado), 200

@app.route('/domiciliarios/ranking', methods=['GET'])
def ranking_domiciliarios():
    ranking = sorted(domiciliarios, key=lambda x: x['EstrellasCalificacion'], reverse=True)
    return jsonify(ranking), 200

if __name__ == '__main__':
