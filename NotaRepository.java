package cl.uchile.dcc.cc5002.tarea4.repository;

import cl.uchile.dcc.cc5002.tarea4.model.Nota;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;

public interface NotaRepository extends JpaRepository<Nota, Integer> {

    List<Nota> findByAvistamientoId(Integer avistamientoId);
}