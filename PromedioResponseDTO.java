package cl.uchile.dcc.cc5002.tarea4.dto;

public record PromedioResponseDTO(
        Integer avistamientoId,
        String promedioNota,
        int totalNotas
) {
}