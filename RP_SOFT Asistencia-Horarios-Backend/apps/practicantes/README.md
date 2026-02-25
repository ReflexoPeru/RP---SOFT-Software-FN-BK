# Módulo: Gestión de Practicantes

## 1. Descripción del Módulo

Este módulo se encarga de la gestión de la información de los practicantes, incluyendo sus datos personales, estado y estadísticas.

- **Responsabilidad principal:** CRUD de practicantes y exposición de estadísticas.
- **Relación con otros módulos:** Es la base para otros módulos como `gestion` y `puntualidad` que necesitan acceder a la información de los practicantes.
- **Arquitectura Hexagonal:**
  - **Dominio:** Define la entidad `Practicante` con su lógica de negocio y el `PracticanteRepository` como puerto de salida para la persistencia.
  - **Aplicación:** El `PracticanteService` orquesta las operaciones sobre los practicantes.
  - **Infraestructura:** Proporciona la implementación concreta del repositorio con Django ORM, las vistas de DRF y los serializers.

## 2. Documentación de Endpoints

### `GET /api/practicantes/`

- **Método HTTP:** `GET`
- **Descripción:** Lista todos los practicantes.
- **Servicio de Aplicación:** `PracticanteService.get_all_practicantes`
- **Ejemplo de Respuesta:**
  ```json
  [
    {
      "id": 1,
      "id_discord": 12345,
      "nombre": "Juan",
      "apellido": "Pérez",
      "correo": "juan.perez@example.com",
      "semestre": 5,
      "estado": "activo"
    }
  ]
  ```

### `POST /api/practicantes/`

- **Método HTTP:** `POST`
- **Descripción:** Crea un nuevo practicante.
- **Servicio de Aplicación:** `PracticanteService.create_practicante`
- **Ejemplo de Request:**
  ```json
  {
    "id_discord": 12345,
    "nombre": "Juan",
    "apellido": "Pérez",
    "correo": "juan.perez@example.com",
    "semestre": 5,
    "estado": "activo"
  }
  ```
- **Ejemplo de Respuesta:** `201 Created` con el objeto del practicante creado.

### `GET /api/practicantes/<int:pk>/`

- **Método HTTP:** `GET`
- **Descripción:** Obtiene un practicante por su ID.
- **Servicio de Aplicación:** `PracticanteService.get_practicante_by_id`
- **Ejemplo de Respuesta:**
  ```json
  {
    "id": 1,
    "id_discord": 12345,
    "nombre": "Juan",
    "apellido": "Pérez",
    "correo": "juan.perez@example.com",
    "semestre": 5,
    "estado": "activo"
  }
  ```

### `PUT /api/practicantes/<int:pk>/`

- **Método HTTP:** `PUT`
- **Descripción:** Actualiza un practicante existente.
- **Servicio de Aplicación:** `PracticanteService.update_practicante`
- **Ejemplo de Request:**
  ```json
  {
    "semestre": 6,
    "estado": "en_recuperacion"
  }
  ```

### `DELETE /api/practicantes/<int:pk>/`

- **Método HTTP:** `DELETE`
- **Descripción:** Elimina un practicante.
- **Servicio de Aplicación:** `PracticanteService.delete_practicante`
- **Respuesta:** `204 No Content`

### `GET /api/practicantes/estadisticas/`

- **Método HTTP:** `GET`
- **Descripción:** Obtiene estadísticas sobre los practicantes.
- **Servicio de Aplicación:** `PracticanteService.get_practicante_stats`
- **Ejemplo de Respuesta:**
  ```json
  {
    "total": 10,
    "activos": 7,
    "en_recuperacion": 2,
    "en_riesgo": 1
  }
  ```

### `GET /api/practicantes/advertencias/mes/`

- **Descripción:** Obtiene las advertencias del mes actual.

### `GET /api/practicantes/advertencias/historico/`

- **Descripción:** Obtiene el histórico de advertencias.

### `GET /api/practicantes/permisos/semana/`

- **Descripción:** Obtiene los permisos de la semana actual.

### `GET /api/practicantes/permisos/practicante/`

- **Descripción:** Obtiene los permisos por practicante.

### `GET /api/practicantes/exportar/semanal/`

- **Descripción:** Exporta el reporte semanal en formato Excel.

### `GET /api/practicantes/exportar/mensual/`

- **Descripción:** Exporta el reporte mensual en formato Excel.

## 4. Requisitos y Configuración

- **Dependencias:** Django, djangorestframework.
- **Migraciones:** Requiere que las migraciones del módulo se hayan ejecutado.

## 5. Buenas Prácticas y Estándares

- **Convenciones:** Sigue las convenciones de DRF con ViewSets para las operaciones CRUD.
- **Extensibilidad:** Añadir nuevos endpoints se puede hacer a través de acciones personalizadas en el `PracticanteViewSet` o creando nuevas vistas de API. La lógica de negocio debe residir en el `PracticanteService`.
- **Desacoplamiento:** El dominio está aislado del framework, permitiendo que la lógica de negocio se pruebe de forma independiente.
