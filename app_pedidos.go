package main

import (
	"bytes"
	"encoding/json"
	"io/ioutil"
	"net/http"

	"github.com/gorilla/mux"
)

type Pedido struct {
	ID        int     `json:"id"`
	Cliente   string  `json:"cliente"`
	Direccion string  `json:"direccion"`
	Items     []Item  `json:"items"`
	Total     float64 `json:"total"`
}

type Item struct {
	Nombre   string  `json:"nombre"`
	Cantidad int     `json:"cantidad"`
	Precio   float64 `json:"precio"`
}

type Domiciliario struct {
	ID                    int        `json:"id_Domiciliario"`
	Nombre                string     `json:"Nombre"`
	UbicacionDomiciliario [2]float64 `json:"UbicacionDomiciliario"`
	Taria                 float64    `json:"Taria"`
	FotoDomiciliario      string     `json:"FotoDomiciliario"`
	TipoVehiculo          string     `json:"TipoVehiculo"`
	EstrellasCalificacion int        `json:"EstrellasCalificacion"`
	ImagenAsignacion      string     `json:"ImagenAsignacion,omitempty"`
}

var pedidos []Pedido

func crearPedido(w http.ResponseWriter, r *http.Request) {
	var nuevoPedido Pedido
	err := json.NewDecoder(r.Body).Decode(&nuevoPedido)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}
	nuevoPedido.ID = len(pedidos) + 1
	pedidos = append(pedidos, nuevoPedido)
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(nuevoPedido)
}

func obtenerPedidos(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(pedidos)
}

func obtenerDomiciliariosCercanos(w http.ResponseWriter, r *http.Request) {
	// Simulación de la ubicación del establecimiento
	ubicacionEstablecimiento := [2]float64{4.60971, -74.08175}

	// Crear el payload para enviar al microservicio de Python
	payload := map[string][2]float64{
		"UbicacionEstablecimiento": ubicacionEstablecimiento,
	}
	payloadBytes, _ := json.Marshal(payload)

	// Hacer la solicitud HTTP al microservicio de Python
	resp, err := http.Post("http://localhost:5000/domiciliarios/cercanos", "application/json", bytes.NewBuffer(payloadBytes))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer resp.Body.Close()

	// Leer la respuesta del microservicio de Python
	body, _ := ioutil.ReadAll(resp.Body)

	var domiciliariosCercanos []Domiciliario
	json.Unmarshal(body, &domiciliariosCercanos)

	// Devolver la respuesta al cliente
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	w.Write(body)
}

func main() {
	router := mux.NewRouter()

	router.HandleFunc("/pedido", crearPedido).Methods("POST")
	router.HandleFunc("/pedidos", obtenerPedidos).Methods("GET")
	router.HandleFunc("/domiciliarios/cercanos", obtenerDomiciliariosCercanos).Methods("GET")

	http.ListenAndServe(":5001", router)
}
