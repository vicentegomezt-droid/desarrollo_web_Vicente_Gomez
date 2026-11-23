package cl.uchile.dcc.cc5002.tarea4.dto;

public record AvistamientoDTO(
        Integer id,
        String nombreVoluntario,
        String diaAvistamiento,
        String nombreAve,
        String nombreComuna,
        String promedioNota
) {
}