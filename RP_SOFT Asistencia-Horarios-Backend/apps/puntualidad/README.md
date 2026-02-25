# Módulo: Puntualidad y Asistencia

## 1. Descripción del Módulo

Este módulo gestiona la puntualidad y asistencia de los practicantes, incluyendo el registro de asistencias, justificaciones y recuperaciones de horas.

- **Responsabilidad principal:** Monitorear y gestionar la asistencia de los practicantes.
- **Relación con otros módulos:** Depende del módulo de `practicantes` para obtener la información de los mismos.
- **Arquitectura Hexagonal:**
  - **Dominio:** Define las entidades `Asistencia`, `HorarioClases`, `AsistenciaRecuperacion`, y sus respectivos repositorios.
  - **Aplicación:** Contiene los servicios para los casos de uso, como `ResumenPuntualidadService`, `CrearJustificacionService`, etc.
  - **Infraestructura:** Implementa las vistas, serializers y repositorios utilizando Django y DRF.

## 2. Documentación de Endpoints

### `GET /api/puntualidad/resumen/`

- **Descripción:** Devuelve un resumen de la puntualidad del día actual.
- **Servicio de Aplicación:** `ResumenPuntualidadService`
- **Ejemplo de Respuesta:**
  ```json
  {
    "asistencias": 10,
    "tardanzas": 2,
    "faltas": 3,
    "total": 15,
    "con_clases": 12,
    "ausentes_justificados": 1,
    "ausentes_sin_justificar": 2
  }
  ```

### `GET /api/puntualidad/alertas/`

- **Descripción:** Devuelve alertas automáticas de puntualidad.
- **Servicio de Aplicación:** `AlertasPuntualidadService`
- **Ejemplo de Respuesta:**
  ```json
  [
    {
      "tipo": "tardanza",
      "titulo": "Tardanza potencial detectada",
      "cantidad": 2,
      "hora": "8:05 a.m.",
      "descripcion": "Gracia de 5 minutos aplicada",
      "practicantes": ["Juan Pérez", "Ana Gómez"]
    }
  ]
  ```

### `GET /api/puntualidad/practicantes/`

- **Descripción:** Devuelve la lista de practicantes con su estado de asistencia del día.
- **Ejemplo de Respuesta:**
  ```json
  [
    {
      "id": 1,
      "nombre": "Juan",
      "apellido": "Pérez",
      "equipo": "Rpsoft",
      "team": "Team Alpha",
      "horaIngreso": "08:10 AM",
      "horasSemanales": "24/30",
      "horasCompletadas": 24,
      "horasTotales": 30,
      "estado": "tardanza",
      "ticket": "TKT-123 - Cita médica"
    }
  ]
  ```

### `GET /api/puntualidad/justificaciones/`

- **Descripción:** Devuelve la lista de justificaciones.
- **Servicio de Aplicación:** `ListarJustificacionesService`

### `POST /api/puntualidad/justificaciones/crear/`

- **Descripción:** Crea una nueva justificación.
- **Servicio de Aplicación:** `CrearJustificacionService`
- **Request Body:** `JustificacionCreateSerializer`
- **Ejemplo de Request:**
  ```json
  {
    "practicante_id": 1,
    "fecha": "2023-10-27",
    "motivo": "Cita médica",
    "ticket_id": "TKT-123"
  }
  ```

### `POST /api/puntualidad/justificaciones/<int:pk>/aprobar/`

- **Descripción:** Aprueba una justificación.
- **Servicio de Aplicación:** `AprobarJustificacionService`

### `POST /api/puntualidad/justificaciones/<int:pk>/rechazar/`

- **Descripción:** Rechaza una justificación.
- **Servicio de Aplicación:** `RechazarJustificacionService`
- **Request Body:**
  ```json
  {
    "motivo_rechazo": "Falta de evidencia"
  }
  ```

### `GET /api/puntualidad/recuperaciones/`

- **Descripción:** Devuelve la lista de recuperaciones de horas.
- **Servicio de Aplicación:** `ListarRecuperacionesService`

### `GET /api/puntualidad/practicantes/activos/`

- **Descripción:** Devuelve una lista simple de practicantes activos.

## 4. Requisitos y Configuración

- **Dependencias:** Django, djangorestframework.
- **Migraciones:** Requiere que las migraciones del módulo se hayan ejecutado.

## 5. Buenas Prácticas y Estándares

- **Servicios de Aplicación:** Cada caso de uso está encapsulado en su propio servicio.
- **Validaciones:** Los serializers se utilizan para validar los datos de entrada en los endpoints de creación y actualización.
- **Manejo de Errores:** Las vistas manejan excepciones y devuelven respuestas de error apropiadas.
