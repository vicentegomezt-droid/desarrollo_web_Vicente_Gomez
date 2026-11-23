# Tarea 4

Implementación del buscador reactivo de avistamientos y evaluación de notas usando Spring Boot, Java 17 y JPA, junto con una vista en HTML y JavaScript que se comunica con el backend mediante `fetch`.

## Decisiones y detalles para la corrección

- Dejé `spring.jpa.hibernate.ddl-auto=none` en `application.properties` para que Hibernate no modifique las tablas existentes y la tabla `nota` se maneje con `tabla-nota.sql`.
- Usé variables de entorno con valores por defecto en `application.properties` para la conexión a MySQL, así se puede probar en distintos equipos sin tener que cambiar el archivo.
- En la búsqueda por ave, voluntario o comuna agregué manejo de valores nulos (`COALESCE`) y escapado de texto en el frontend para evitar errores o inyección HTML al resaltar coincidencias.
- Para las notas validé tanto en el frontend como en el servicio que sean enteros entre 1 y 7 (ambos inclusives), devolviendo `"-"` cuando un avistamiento aún no tiene notas y recalculando el promedio al guardar una nueva.
- Moví los archivos de entregas anteriores de Flask a una carpeta aparte para dejar ordenada la estructura de Maven.

## Cómo correrlo

Con MySQL levantado y la tabla `nota` creada, ejecuta en la carpeta `tarea4`:

```bash
mvn spring-boot:run
