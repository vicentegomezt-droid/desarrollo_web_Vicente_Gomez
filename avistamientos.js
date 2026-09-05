 
const tipoFiltro = document.getElementById("tipo-filtro");
const orden = document.getElementById("orden");
const resultados = document.getElementById("resultados");
const paginacion = document.getElementById("paginacion");

// Datos de ejemplo para poder probar la interfaz
const avistamientos = [
    {
        tipo: "rapaz",
        nombre: "Águila",
        lugar: "Cajón del Maipo",
        fecha: "2026-08-20"
    },
    {
        tipo: "marina",
        nombre: "Pelícano",
        lugar: "Valparaíso",
        fecha: "2026-07-15"
    },
    {
        tipo: "acuática",
        nombre: "Cisne de cuello negro",
        lugar: "Valdivia",
        fecha: "2026-08-05"
    },
    {
        tipo: "paseriforme",
        nombre: "Chincol",
        lugar: "Santiago",
        fecha: "2026-08-28"
    },
    {
        tipo: "rapaz",
        nombre: "Tucúquere",
        lugar: "Concepción",
        fecha: "2026-06-10"
    },
    {
        tipo: "acuática",
        nombre: "Tagua",
        lugar: "Puerto Montt",
        fecha: "2026-07-30"
    }
];

const resultadosPorPagina = 3;
let paginaActual = 1;

function mostrarResultados() {

    let lista = [...avistamientos];

    // Filtrar por tipo de ave
    if (tipoFiltro.value !== "") {
        lista = lista.filter(function(avistamiento) {
            return avistamiento.tipo === tipoFiltro.value;
        });
    }

    // Ordenar resultados
    if (orden.value === "fecha-ascendente") {
        lista.sort(function(a, b) {
            return new Date(a.fecha) - new Date(b.fecha);
        });
    }

    if (orden.value === "fecha-descendente") {
        lista.sort(function(a, b) {
            return new Date(b.fecha) - new Date(a.fecha);
        });
    }

    if (orden.value === "lugar-ascendente") {
        lista.sort(function(a, b) {
            return a.lugar.localeCompare(b.lugar);
        });
    }

    // Calcular páginas
    const totalPaginas = Math.ceil(lista.length / resultadosPorPagina);

    if (paginaActual > totalPaginas && totalPaginas > 0) {
        paginaActual = totalPaginas;
    }

    const inicio = (paginaActual - 1) * resultadosPorPagina;
    const fin = inicio + resultadosPorPagina;

    const pagina = lista.slice(inicio, fin);

    // Limpiar resultados anteriores
    resultados.innerHTML = "";

    if (pagina.length === 0) {
        resultados.innerHTML = "<p>No se encontraron avistamientos.</p>";
    } else {

        pagina.forEach(function(avistamiento) {

            const articulo = document.createElement("article");

            const titulo = document.createElement("h3");
            titulo.textContent = avistamiento.nombre;

            const tipo = document.createElement("p");
            tipo.textContent = "Tipo: " + avistamiento.tipo;

            const lugar = document.createElement("p");
            lugar.textContent = "Lugar: " + avistamiento.lugar;

            const fecha = document.createElement("p");
            fecha.textContent = "Fecha: " + avistamiento.fecha;

            articulo.appendChild(titulo);
            articulo.appendChild(tipo);
            articulo.appendChild(lugar);
            articulo.appendChild(fecha);

            resultados.appendChild(articulo);
        });
    }

    mostrarPaginacion(totalPaginas);
}


function mostrarPaginacion(totalPaginas) {

    paginacion.innerHTML = "";

    for (let i = 1; i <= totalPaginas; i++) {

        const boton = document.createElement("button");

        boton.textContent = i;

        boton.addEventListener("click", function() {
            paginaActual = i;
            mostrarResultados();
        });

        paginacion.appendChild(boton);
    }
}


// Filtrar y ordenar nuevamente cada vez que cambia una opción
tipoFiltro.addEventListener("change", function() {
    paginaActual = 1;
    mostrarResultados();
});

orden.addEventListener("change", function() {
    paginaActual = 1;
    mostrarResultados();
});


// Mostrar resultados al abrir la página
mostrarResultados();