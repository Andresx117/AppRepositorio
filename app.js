document.getElementById("btnCercanos").addEventListener("click", function(e) {
    e.preventDefault();
    obtenerDomiciliariosCercanos();
});

document.getElementById("btnPorVehiculo").addEventListener("click", function(e) {
    e.preventDefault();
    const tipo = document.getElementById("tipoVehiculo").value;
    obtenerDomiciliariosPorTipoVehiculo(tipo);
});

document.getElementById("btnRanking").addEventListener("click", function(e) {
    e.preventDefault();
    obtenerRankingDomiciliarios();
});

function obtenerDomiciliariosCercanos() {
    fetch('http://127.0.0.1:5000/domiciliarios/cercanos', {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=UTF-8"
        },
        body: JSON.stringify({ UbicacionEstablecimiento: [4.60971, -74.08175] })
    })
    .then(response => response.json())
    .then((data) => {
        mostrarResultados(data);
    })
    .catch(err => console.log(err));
}

function obtenerDomiciliariosPorTipoVehiculo(tipo) {
    fetch(`http://127.0.0.1:5000/domiciliarios/tipo_vehiculo?tipo=${tipo}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/json;charset=UTF-8"
        }
    })
    .then(response => response.json())
    .then((data) => {
        mostrarResultados(data);
    })
    .catch(err => console.log(err));
}

function obtenerRankingDomiciliarios() {
    fetch('http://127.0.0.1:5000/domiciliarios/ranking', {
        method: "GET",
        headers: {
            "Content-Type": "application/json;charset=UTF-8"
        }
    })
    .then(response => response.json())
    .then((data) => {
        mostrarResultados(data);
    })
    .catch(err => console.log(err));
}

function mostrarResultados(data) {
    const resultados = document.getElementById("resultados");
    resultados.textContent = JSON.stringify(data, null, 2);
}