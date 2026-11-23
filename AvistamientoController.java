package cl.uchile.dcc.cc5002.tarea4.controller;

import cl.uchile.dcc.cc5002.tarea4.dto.AvistamientoDTO;
import cl.uchile.dcc.cc5002.tarea4.dto.NotaRequestDTO;
import cl.uchile.dcc.cc5002.tarea4.dto.PromedioResponseDTO;
import cl.uchile.dcc.cc5002.tarea4.service.AvistamientoService;
import java.util.List;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/api")
public class AvistamientoController {

    private final AvistamientoService avistamientoService;

    public AvistamientoController(AvistamientoService avistamientoService) {
        this.avistamientoService = avistamientoService;
    }

    @GetMapping("/avistamientos")
    public List<AvistamientoDTO> buscarAvistamientos(
            @RequestParam(name = "q", required = false, defaultValue = "") String query
    ) {
        return avistamientoService.buscarAvistamientos(query);
    }

    @PostMapping("/notas")
    public ResponseEntity<?> crearNota(@RequestBody NotaRequestDTO request) {
        try {
            PromedioResponseDTO respuesta = avistamientoService.agregarNota(
                    request != null ? request.avistamientoId() : null,
                    request != null ? request.nota() : null
            );
            return ResponseEntity.status(HttpStatus.CREATED).body(respuesta);
        } catch (ResponseStatusException ex) {
            String mensaje = ex.getReason() != null ? ex.getReason() : "Solicitud inválida.";
            return ResponseEntity.status(ex.getStatusCode())
                    .body(Map.of("error", mensaje));
        }
    }
}