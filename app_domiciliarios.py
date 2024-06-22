import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from math import radians, cos, sin, sqrt, atan2
import urllib.parse

domiciliarios = [
    {
        'id_Domiciliario': 1,
        'Nombre': 'Carlos Sanchez',
        'UbicacionDomiciliario': [4.60971, -74.08175],
        'Taria': 15.5,
        'FotoDomiciliario': 'foto1.jpg',
        'TipoVehiculo': 'Moto',
        'EstrellasCalificacion': 4
    },
    {
        'id_Domiciliario': 2,
        'Nombre': 'Maria Perez',
        'UbicacionDomiciliario': [4.61577, -74.07021],
        'Taria': 10.0,
        'FotoDomiciliario': 'foto2.jpg',
        'TipoVehiculo': 'Bicicleta',
        'EstrellasCalificacion': 5
    },
    {
        'id_Domiciliario': 3,
        'Nombre': 'Juan Lopez',
        'UbicacionDomiciliario': [4.6000, -74.0833],
        'Taria': 12.0,
        'FotoDomiciliario': 'foto3.jpg',
        'TipoVehiculo': 'Moto',
        'EstrellasCalificacion': 3
    },
    # ... más domiciliarios
]

def calcular_distancia(coord1, coord2):
    R = 6373.0  # radio de la Tierra en km

    lat1, lon1 = map(radians, coord1)
    lat2, lon2 = map(radians, coord2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c
    return distancia

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == '/domiciliarios/tipo_vehiculo':
            tipo = query.get('tipo', [None])[0]
            if tipo:
                self.obtener_domiciliarios_por_tipo_vehiculo(tipo)
            else:
                self._set_headers(400)
                self.wfile.write(json.dumps({'error': 'Tipo de vehiculo no especificado'}).encode())
        elif path == '/domiciliarios/ranking':
            self.ranking_domiciliarios()
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        if self.path == '/domiciliarios/cercanos':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            self.obtener_domiciliarios_cercanos(data)
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def obtener_domiciliarios_cercanos(self, data):
        ubicacion_establecimiento = data.get('UbicacionEstablecimiento')
        if not ubicacion_establecimiento:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'Ubicacion del establecimiento no especificada'}).encode())
            return

        domiciliarios_ordenados = sorted(domiciliarios, key=lambda x: calcular_distancia(x['UbicacionDomiciliario'], ubicacion_establecimiento))
        tres_cercanos = domiciliarios_ordenados[:3]
        
        for d in tres_cercanos:
            d['ImagenAsignacion'] = d['FotoDomiciliario']

        self._set_headers(200)
        self.wfile.write(json.dumps(tres_cercanos).encode())

    def obtener_domiciliarios_por_tipo_vehiculo(self, tipo):
        resultado = [d for d in domiciliarios if d['TipoVehiculo'].lower() == tipo.lower()]
        self._set_headers(200)
        self.wfile.write(json.dumps(resultado).encode())

    def ranking_domiciliarios(self):
        ranking = sorted(domiciliarios, key=lambda x: x['EstrellasCalificacion'], reverse=True)
        self._set_headers(200)
        self.wfile.write(json.dumps(ranking).encode())

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}')
    httpd.serve_forever()

if __name__ == '__main__':
    run()