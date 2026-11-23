package cl.uchile.dcc.cc5002.tarea4.service;

import cl.uchile.dcc.cc5002.tarea4.dto.AvistamientoDTO;
import cl.uchile.dcc.cc5002.tarea4.dto.PromedioResponseDTO;
import cl.uchile.dcc.cc5002.tarea4.model.Avistamiento;
import cl.uchile.dcc.cc5002.tarea4.model.Nota;
import cl.uchile.dcc.cc5002.tarea4.repository.AvistamientoRepository;
import cl.uchile.dcc.cc5002.tarea4.repository.NotaRepository;
import java.util.List;
import java.util.Locale;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

@Service
public class AvistamientoService {

    private final AvistamientoRepository avistamientoRepository;
    private final NotaRepository notaRepository;

    public AvistamientoService(
            AvistamientoRepository avistamientoRepository,
            NotaRepository notaRepository
    ) {
        this.avistamientoRepository = avistamientoRepository;
        this.notaRepository = notaRepository;
    }

    @Transactional(readOnly = true)
    public List<AvistamientoDTO> buscarAvistamientos(String query) {
        String limpio = query == null ? "" : query.trim();
        List<Avistamiento> encontrados = limpio.isEmpty()
                ? avistamientoRepository.findAll()
                : avistamientoRepository.buscarPorTermino(limpio);

        return encontrados.stream()
                .map(this::mapearADto)
                .toList();
    }

    @Transactional
    public PromedioResponseDTO agregarNota(Integer avistamientoId, Integer valorNota) {
        if (avistamientoId == null) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Debe indicar un avistamiento válido.");
        }
        if (valorNota == null || valorNota < 1 || valorNota > 7) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "La nota debe ser un número entero entre 1 y 7, ambos inclusives."
            );
        }

        Avistamiento avistamiento = avistamientoRepository.findById(avistamientoId)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND,
                        "No se encontró el avistamiento solicitado."
                ));

        Nota nuevaNota = new Nota(avistamiento, valorNota);
        notaRepository.save(nuevaNota);

        List<Nota> notasAvistamiento = notaRepository.findByAvistamientoId(avistamientoId);
        String promedioFormateado = calcularPromedio(notasAvistamiento);

        return new PromedioResponseDTO(
                avistamientoId,
                promedioFormateado,
                notasAvistamiento.size()
        );
    }

    private AvistamientoDTO mapearADto(Avistamiento avistamiento) {
        String nombreVoluntario = (avistamiento.getVoluntario() != null && avistamiento.getVoluntario().getNombre() != null)
                ? avistamiento.getVoluntario().getNombre()
                : "";
        String dia = avistamiento.getDiaAvistamiento() != null ? avistamiento.getDiaAvistamiento() : "";
        String ave = avistamiento.getNombreAve() != null ? avistamiento.getNombreAve() : "";
        String comuna = avistamiento.getNombreComuna() != null ? avistamiento.getNombreComuna() : "";

        List<Nota> notas = notaRepository.findByAvistamientoId(avistamiento.getId());
        String promedio = calcularPromedio(notas);

        return new AvistamientoDTO(
                avistamiento.getId(),
                nombreVoluntario,
                dia,
                ave,
                comuna,
                promedio
        );
    }

    private String calcularPromedio(List<Nota> notas) {
        if (notas == null || notas.isEmpty()) {
            return "-";
        }
        double suma = 0.0;
        int validas = 0;
        for (Nota n : notas) {
            if (n.getNota() != null) {
                suma += n.getNota();
                validas++;
            }
        }
        if (validas == 0) {
            return "-";
        }
        return String.format(Locale.US, "%.1f", suma / validas);
    }
}