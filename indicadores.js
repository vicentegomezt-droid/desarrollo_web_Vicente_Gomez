const cantidadVoluntarios = document.getElementById("cantidad-voluntarios");
const cantidadAvistamientos = document.getElementById("cantidad-avistamientos");
const graficoTipos = document.getElementById("grafico-tipos");

// Datos de ejemplo
const voluntarios = [
    "Juan",
    "Pedro",
    "María",
    "Ana",
    "Sofía"
];

const avistamientos = [
    { tipo: "rapaz" },
    { tipo: "rapaz" },
    { tipo: "marina" },
    { tipo: "acuática" },
    { tipo: "acuática" },
    { tipo: "paseriforme" }
];


// Mostrar cantidad de voluntarios
cantidadVoluntarios.textContent =
    "Voluntarios registrados: " + voluntarios.length;


// Mostrar cantidad de avistamientos
cantidadAvistamientos.textContent =
    "Avistamientos registrados: " + avistamientos.length;


// Contar avistamientos por tipo
const cantidadPorTipo = {};

avistamientos.forEach(function(avistamiento) {

    if (cantidadPorTipo[avistamiento.tipo] === undefined) {
        cantidadPorTipo[avistamiento.tipo] = 1;
    } else {
        cantidadPorTipo[avistamiento.tipo]++;
    }

});


 // Mostrar los resultados como barras
for (const tipo in cantidadPorTipo) {

    const contenedor = document.createElement("div");

    const nombre = document.createElement("p");
    nombre.textContent =
        tipo + ": " + cantidadPorTipo[tipo] + " avistamientos";

    const barra = document.createElement("div");
    barra.style.width = (cantidadPorTipo[tipo] * 100) + "px";
    barra.style.height = "20px";

    contenedor.appendChild(nombre);
    contenedor.appendChild(barra);

    graficoTipos.appendChild(contenedor);
}