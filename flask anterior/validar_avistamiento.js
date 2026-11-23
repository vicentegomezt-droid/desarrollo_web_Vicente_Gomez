document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("form-avistamiento");
    const errorBox = document.getElementById("js-error-box");

    if (!form || !errorBox) return;

    const extensionesPermitidas = ["png", "jpg", "jpeg", "gif", "webp", "mp4", "webm", "mov"];

    function mostrarErrores(errores) {
        errorBox.innerHTML = "<ul class='mb-0'>" + errores.map(e => `<li>${e}</li>`).join("") + "</ul>";
        errorBox.classList.remove("d-none");
        errorBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function ocultarErrores() {
        errorBox.innerHTML = "";
        errorBox.classList.add("d-none");
    }

    form.addEventListener("submit", function (event) {
        const errores = [];

        const voluntario = document.getElementById("voluntario_id").value.trim();
        const tipoAve = document.getElementById("tipo_ave").value.trim();
        const nombreAve = document.getElementById("nombre_ave").value.trim();
        const lugar = document.getElementById("lugar").value.trim();
        const fechaStr = document.getElementById("fecha").value.trim();
        const horaStr = document.getElementById("hora").value.trim();
        const archivoInput = document.getElementById("archivo");

        if (!voluntario || !tipoAve || !nombreAve || !lugar || !fechaStr || !horaStr) {
            errores.push("Todos los campos del avistamiento son obligatorios.");
        }

        if (fechaStr) {
            const partes = fechaStr.split("-");
            if (partes.length === 3) {
                const anio = parseInt(partes[0], 10);
                const mes = parseInt(partes[1], 10) - 1;
                const dia = parseInt(partes[2], 10);
                const fechaIngresada = new Date(anio, mes, dia);

                const hoy = new Date();
                hoy.setHours(0, 0, 0, 0);

                if (isNaN(fechaIngresada.getTime())) {
                    errores.push("La fecha ingresada no es válida.");
                } else if (anio < 1900) {
                    errores.push("La fecha debe ser desde el año 1900 en adelante.");
                } else if (fechaIngresada > hoy) {
                    errores.push("No puedes registrar un avistamiento en una fecha futura.");
                }
            } else {
                errores.push("El formato de fecha no es válido.");
            }
        }

        if (!archivoInput || !archivoInput.files || archivoInput.files.length === 0) {
            errores.push("Debes adjuntar una imagen o video del avistamiento.");
        } else {
            const archivo = archivoInput.files[0];
            const nombreArchivo = archivo.name || "";
            const ext = nombreArchivo.includes(".") ? nombreArchivo.split(".").pop().toLowerCase() : "";
            if (!extensionesPermitidas.includes(ext)) {
                errores.push("Formato de archivo no permitido. Usa una imagen (png, jpg, jpeg, gif, webp) o video (mp4, webm, mov).");
            }
        }

        if (errores.length > 0) {
            event.preventDefault();
            mostrarErrores(errores);
        } else {
            ocultarErrores();
        }
    });
});