package cl.uchile.dcc.cc5002.tarea4.model;

import jakarta.persistence.*;
import java.util.ArrayList;
import java.util.List;

@Entity
@Table(name = "avistamiento")
public class Avistamiento {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @ManyToOne(fetch = FetchType.EAGER)
    @JoinColumn(name = "voluntario_id")
    private Voluntario voluntario;

    @Column(name = "dia_avistamiento")
    private String diaAvistamiento;

    @Column(name = "nombre_ave")
    private String nombreAve;

    @Column(name = "nombre_comuna")
    private String nombreComuna;

    @OneToMany(mappedBy = "avistamiento", fetch = FetchType.LAZY)
    private List<Nota> notas = new ArrayList<>();

    public Avistamiento() {
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Voluntario getVoluntario() {
        return voluntario;
    }

    public void setVoluntario(Voluntario voluntario) {
        this.voluntario = voluntario;
    }

    public String getDiaAvistamiento() {
        return diaAvistamiento;
    }

    public void setDiaAvistamiento(String diaAvistamiento) {
        this.diaAvistamiento = diaAvistamiento;
    }

    public String getNombreAve() {
        return nombreAve;
    }

    public void setNombreAve(String nombreAve) {
        this.nombreAve = nombreAve;
    }

    public String getNombreComuna() {
        return nombreComuna;
    }

    public void setNombreComuna(String nombreComuna) {
        this.nombreComuna = nombreComuna;
    }

    public List<Nota> getNotas() {
        return notas;
    }

    public void setNotas(List<Nota> notas) {
        this.notas = notas;
    }
}