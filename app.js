const buscadorInput = document.getElementById("buscadorInput");
const tablaCuerpo = document.getElementById("tablaCuerpo");
const mensajeEstado = document.getElementById("mensajeEstado");

let controladorAbort = null;

function escaparHtml(texto) {
    if (texto === null || texto === undefined) return "";
    return String(texto)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function escaparRegex(texto) {
    return texto.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function resaltarCoincidencia(texto, termino) {
    const seguro = escaparHtml(texto);
    const limpio = (termino || "").trim();
    if (!limpio) {
        return seguro;
    }
    const regex = new RegExp(`(${escaparRegex(limpio)})`, "gi");
    return seguro.replace(regex, "<mark>$1</mark>");
}

function mostrarMensaje(texto, tipo = "") {
    mensajeEstado.textContent = texto || "";
    mensajeEstado.className = "mensaje-estado";
    if (tipo === "error") {
        mensajeEstado.classList.add("mensaje-error");
    } else if (tipo === "vacio") {
        mensajeEstado.classList.add("mensaje-vacio");
    }
}

function renderizarFilas(avistamientos, termino) {
    tablaCuerpo.innerHTML = "";

    if (!Array.isArray(avistamientos) || avistamientos.length === 0) {
        const msg = termino && termino.trim() !== ""
            ? `No se encontraron avistamientos para "${termino.trim()}".`
            : "No hay avistamientos registrados.";
        mostrarMensaje(msg, "vacio");
        return;
    }

    mostrarMensaje("");

    avistamientos.forEach((av) => {
        const tr = document.createElement("tr");
        const promedioTexto = av.promedioNota ? escaparHtml(av.promedioNota) : "-";

        tr.innerHTML = `
            <td>${escaparHtml(av.diaAvistamiento)}</td>
            <td>${resaltarCoincidencia(av.nombreAve, termino)}</td>
            <td>${resaltarCoincidencia(av.nombreVoluntario, termino)}</td>
            <td>${resaltarCoincidencia(av.nombreComuna, termino)}</td>
            <td id="promedio-${av.id}"><strong>${promedioTexto}</strong></td>
            <td>
                <form class="evaluar-form" data-id="${av.id}">
                    <input
                        type="number"
                        name="nota"
                        min="1"
                        max="7"
                        step="1"
                        placeholder="1-7"
                        required
                    />
                    <button type="submit">Guardar</button>
                </form>
            </td>
        `;
        tablaCuerpo.appendChild(tr);
    });
}

async function cargarAvistamientos(termino = "") {
    if (controladorAbort) {
        controladorAbort.abort();
    }
    controladorAbort = new AbortController();

    try {
        const url = `/api/avistamientos?q=${encodeURIComponent(termino.trim())}`;
        const resp = await fetch(url, { signal: controladorAbort.signal });
        if (!resp.ok) {
            throw new Error("No se pudieron cargar los avistamientos.");
        }
        const datos = await resp.json();
        renderizarFilas(datos, termino);
    } catch (err) {
        if (err.name === "AbortError") {
            return;
        }
        tablaCuerpo.innerHTML = "";
        mostrarMensaje(err.message || "Error al consultar el servidor.", "error");
    }
}

buscadorInput.addEventListener("input", (e) => {
    cargarAvistamientos(e.target.value);
});

tablaCuerpo.addEventListener("submit", async (e) => {
    const form = e.target.closest(".evaluar-form");
    if (!form) return;
    e.preventDefault();

    const avistamientoId = Number(form.dataset.id);
    const inputNota = form.querySelector('input[name="nota"]');
    const rawValor = (inputNota.value || "").trim();

    if (!/^[1-7]$/.test(rawValor)) {
        mostrarMensaje("La nota debe ser un número entero entre 1 y 7, ambos inclusives.", "error");
        inputNota.focus();
        return;
    }

    const valorEntero = Number(rawValor);

    try {
        const resp = await fetch("/api/notas", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                avistamientoId: avistamientoId,
                nota: valorEntero
            })
        });

        const data = await resp.json();
        if (!resp.ok) {
            mostrarMensaje(data.error || "No se pudo guardar la nota.", "error");
            return;
        }

        const celdaPromedio = document.getElementById(`promedio-${avistamientoId}`);
        if (celdaPromedio) {
            celdaPromedio.innerHTML = `<strong>${escaparHtml(data.promedioNota || "-")}</strong>`;
        }
        inputNota.value = "";
        mostrarMensaje(`Nota ${valorEntero} registrada. Nuevo promedio: ${data.promedioNota}.`);
    } catch (err) {
        mostrarMensaje("Error de red al guardar la nota.", "error");
    }
});

cargarAvistamientos("");