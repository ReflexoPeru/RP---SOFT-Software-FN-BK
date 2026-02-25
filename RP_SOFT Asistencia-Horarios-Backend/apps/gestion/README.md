# Módulo: Horarios y Recuperaciones

## 1. Descripción del Módulo

Este módulo se encarga de la gestión de practicantes, horarios, y procesos de recuperación de clases. Proporciona una visión general del estado de los practicantes y sus horarios, y permite a los administradores gestionar las solicitudes de recuperación.

- **Responsabilidad principal:** Gestionar la información de los practicantes, sus horarios y las solicitudes de recuperación de clases.
- **Relación con otros módulos:** Este módulo interactúa con el módulo de `practicantes` para obtener la información de los mismos.
- **Arquitectura Hexagonal:**
  - **Dominio:** Define las entidades de negocio como `Practicante` y los contratos de los repositorios (`PracticanteRepository`, `AsistenciaRepository`, `HorarioRepository`, `AdvertenciaRepository`).
  - **Aplicación:** Contiene los servicios que orquestan los casos de uso del negocio, como `DashboardService`, `HorarioService`, y `RecuperacionService`.
  - **Infraestructura:** Implementa los detalles de la tecnología, incluyendo vistas de Django, serializers, y la implementación de los repositorios con el ORM de Django.

## 2. Documentación de Endpoints

### Dashboard

#### `GET /api/gestion/dashboard/summary/`

-   **Descripción:** Obtiene un resumen del estado de los practicantes.
-   **Servicio de Aplicación:** `DashboardService.get_summary`
-   **Ejemplo de Respuesta:**
    ```json
    {
      "practicantes_con_horario": "0/0",
      "clases_hoy": 0,
      "clases_parciales": 0,
      "sin_horario_registrado": 0
    }
    ```

### Horarios

#### `GET /api/gestion/horarios/semanales/`

-   **Descripción:** Obtiene una vista semanal de los horarios.
-   **Servicio de Aplicación:** `HorarioService.get_vista_semanal`
-   **Ejemplo de Respuesta:**
    ```json
    {
      "lunes": [],
      "martes": [],
      "miercoles": [],
      "jueves": [],
      "viernes": []
    }
    ```

### Practicantes

#### `GET /api/gestion/practicantes/`

-   **Descripción:** Lista todos los practicantes con su información básica.
-   **Repositorio:** `PracticanteRepository.list_all_with_horario`
-   **Ejemplo de Respuesta:**
    ```json
    [
      {
        "id": 1,
        "nombre": "Juan Pérez",
        "servidor": "Rpsoft",
        "horario_completo": true
      }
    ]
    ```

#### `GET /api/gestion/practicantes/<int:practicante_id>/horario/`

-   **Descripción:** Obtiene el horario de un practicante específico.
-   **Repositorio:** `PracticanteRepository.get_with_horario`
-   **Ejemplo de Respuesta:**
    ```json
    [
      {
        "id": 1,
        "dia": "lunes"
      }
    ]
    ```

#### `POST /api/gestion/practicantes/<int:practicante_id>/horario/actualizar/`

-   **Descripción:** Actualiza el horario de un practicante.
-   **Servicio de Aplicación:** `HorarioService.actualizar_horario`
-   **Parámetros:**
    -   `body`: Datos del horario a actualizar.
-   **Ejemplo de Respuesta:**
    ```json
    {
      "message": "Horario actualizado"
    }
    ```

#### `POST /api/gestion/practicantes/<int:practicante_id>/registrar/`

-   **Descripción:** Registra un horario con evidencia fotográfica.
-   **Servicio de Aplicación:** `HorarioService.registrar_con_evidencia`
-   **Parámetros:**
    -   `body`: `foto` (archivo) y `bloques` (JSON).
-   **Ejemplo de Respuesta:**
    ```json
    {
      "message": "Horario enviado para aprobación"
    }
    ```

### Recuperaciones

#### `GET /api/gestion/recuperaciones/pendientes/`

-   **Descripción:** Obtiene la lista de recuperaciones pendientes de aprobación.
-   **Servicio de Aplicación:** `RecuperacionService.get_pendientes`
-   **Ejemplo de Respuesta:** `[]` (vacío por defecto en el servicio)

#### `GET /api/gestion/recuperaciones/<int:id>/`

-   **Descripción:** Obtiene el detalle de una solicitud de recuperación.
-   **Servicio de Aplicación:** `RecuperacionService.get_by_id`
-   **Ejemplo de Respuesta:** `{}` (vacío por defecto en el servicio)

#### `POST /api/gestion/recuperaciones/<int:id>/aprobar/`

-   **Descripción:** Aprueba una solicitud de recuperación.
-   **Servicio de Aplicación:** `RecuperacionService.aprobar`
-   **Ejemplo de Respuesta:**
    ```json
    {
      "message": "Recuperación aprobada"
    }
    ```

#### `POST /api/gestion/recuperaciones/<int:id>/rechazar/`

-   **Descripción:** Rechaza una solicitud de recuperación.
-   **Servicio de Aplicación:** `RecuperacionService.rechazar`
-   **Parámetros:**
    -   `body`: `motivo` (string).
-   **Ejemplo de Respuesta:**
    ```json
    {
      "message": "Recuperación rechazada"
    }
    ```

### Servidores

#### `GET /api/gestion/servidores/`

-   **Descripción:** Obtiene la lista de servidores disponibles.
-   **Respuesta Estática:**
    ```json
    ["Rpsoft", "SENATI", "Innovación", "MiniBootcamp", "Laboratorios", "Recuperación"]
    ```

## 4. Requisitos y Configuración

-   **Dependencias:** Django.
-   **Migraciones:** Requiere que las migraciones de los modelos de `gestion` y `practicantes` se hayan ejecutado.

## 5. Buenas Prácticas y Estándares

-   **Convenciones de Nombres:**
    -   Servicios: `*Service` (e.g., `HorarioService`).
    -   Repositorios: `*Repository` (e.g., `PracticanteRepository`).
-   **Extensibilidad:** Para añadir nueva funcionalidad, se deben crear nuevos servicios en la capa de aplicación y, si es necesario, nuevos repositorios y entidades en el dominio. Las vistas en la capa de infraestructura deben ser lo más delgadas posible, delegando la lógica de negocio a los servicios de aplicación.
-   **Desacoplamiento del ORM:** El dominio está completamente desacoplado del ORM de Django. Los servicios de aplicación interactúan con las abstracciones de los repositorios, no con los modelos de Django directamente.
