package cl.uchile.dcc.cc5002.tarea4.repository;

import cl.uchile.dcc.cc5002.tarea4.model.Avistamiento;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface AvistamientoRepository extends JpaRepository<Avistamiento, Integer> {

    @Query("""
            SELECT DISTINCT a
            FROM Avistamiento a
            LEFT JOIN a.voluntario v
            WHERE LOWER(COALESCE(a.nombreAve, '')) LIKE LOWER(CONCAT('%', :termino, '%'))
               OR LOWER(COALESCE(v.nombre, '')) LIKE LOWER(CONCAT('%', :termino, '%'))
               OR LOWER(COALESCE(a.nombreComuna, '')) LIKE LOWER(CONCAT('%', :termino, '%'))
            """)
    List<Avistamiento> buscarPorTermino(@Param("termino") String termino);
}