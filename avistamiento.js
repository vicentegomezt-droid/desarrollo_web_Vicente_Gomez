const formulario = document.getElementById("formulario-avistamiento");

const tipoAve = document.getElementById("tipo-ave");
const nombreAve = document.getElementById("nombre-ave");
const lugar = document.getElementById("lugar");
const fecha = document.getElementById("fecha");
const hora = document.getElementById("hora");
const foto = document.getElementById("foto");
const video = document.getElementById("video");


formulario.addEventListener("submit", function(event) {

    event.preventDefault();

    let errores = [];


    // Validar tipo de ave
    if (tipoAve.value === "") {
        errores.push("Debe seleccionar un tipo de ave.");
    }


    // Validar nombre del ave
    const nombre = nombreAve.value.trim();

    if (nombre.length < 2 || nombre.length > 60) {
        errores.push("El nombre del ave debe tener entre 2 y 60 caracteres.");
    }


    // Validar lugar
    const lugarIngresado = lugar.value.trim();

    if (lugarIngresado.length < 2 || lugarIngresado.length > 100) {
        errores.push("El lugar debe tener entre 2 y 100 caracteres.");
    }


    // Validar fecha
    if (fecha.value === "") {

        errores.push("Debe ingresar una fecha.");

    } else {

        const fechaSeleccionada = new Date(fecha.value + "T00:00:00");

        const hoy = new Date();

        const haceDiezAnios = new Date();
        haceDiezAnios.setFullYear(haceDiezAnios.getFullYear() - 10);

        if (fechaSeleccionada > hoy) {
            errores.push("La fecha del avistamiento no puede ser futura.");
        }

        if (fechaSeleccionada < haceDiezAnios) {
            errores.push("La fecha del avistamiento no puede tener más de 10 años.");
        }
    }


    // Validar hora
    const formatoHora = /^([01]\d|2[0-3]):[0-5]\d$/;

    if (!formatoHora.test(hora.value)) {
        errores.push("Debe ingresar una hora válida.");
    }


    // Validar fotografía
    if (foto.files.length > 0) {

        if (!foto.files[0].type.startsWith("image/")) {
            errores.push("El archivo seleccionado como fotografía no es una imagen válida.");
        }
    }


    // Validar vídeo
    if (video.files.length > 0) {

        if (!video.files[0].type.startsWith("video/")) {
            errores.push("El archivo seleccionado como vídeo no es un vídeo válido.");
        }
    }


    // Debe existir al menos una fotografía o un vídeo
    if (foto.files.length === 0 && video.files.length === 0) {
        errores.push("Debe agregar al menos una fotografía o un vídeo.");
    }


    // Mostrar errores o confirmar registro
    if (errores.length > 0) {

        alert(errores.join("\n"));

    } else {

        alert("El avistamiento se ha registrado correctamente.");

        formulario.reset();
    }

});