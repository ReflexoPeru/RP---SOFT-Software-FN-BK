# Módulo: Reportes

## 1. Descripción del Módulo

Este módulo se encarga de generar y exponer reportes sobre el desempeño de los practicantes, incluyendo horas trabajadas, advertencias y cumplimiento de metas.

- **Responsabilidad principal:** Consolidar y presentar datos de otros módulos en forma de reportes.
- **Relación con otros módulos:** Depende de `practicantes` y `puntualidad` para obtener los datos necesarios.
- **Arquitectura Hexagonal:**
  - **Dominio:** Define el `IReporteRepository` como un puerto para acceder a los datos de los reportes.
  - **Aplicación:** Los servicios de aplicación (`get_dashboard_summary`, `generar_reporte_semanal_excel`, etc.) orquestan la generación de los reportes.
  - **Infraestructura:** Implementa las vistas que exponen los reportes a través de una API REST y funciones para exportar a Excel.

## 2. Documentación de Endpoints

### `GET /api/reportes/summary/`

- **Descripción:** Devuelve un resumen para el dashboard.
- **Servicio de Aplicación:** `get_dashboard_summary`
- **Ejemplo de Respuesta:**
  ```json
  {
    "total_horas": 120.5,
    "meta_semanal": 240,
    "cumplimiento_porcentaje": 50.2,
    "horas_faltantes": 119.5
  }
  ```

### `GET /api/reportes/advertencias/mes/`

- **Descripción:** Devuelve las advertencias del mes actual.
- **Servicio de Aplicación:** `get_advertencias_mes_actual`

### `GET /api/reportes/advertencias/historico/`

- **Descripción:** Devuelve un historial paginado de advertencias.
- **Query Params:** `page`, `size`

### `GET /api/reportes/permisos/semana/`

- **Descripción:** Devuelve los permisos de la semana actual.

### `GET /api/reportes/permisos/practicante/`

- **Descripción:** Devuelve un resumen de permisos por practicante.

### `GET /api/reportes/horas/resumen/`

- **Descripción:** Devuelve un resumen global de horas.

### `GET /api/reportes/horas/detalle/`

- **Descripción:** Devuelve un detalle del cumplimiento de horas.

### `GET /api/reportes/export/semanal/`

- **Descripción:** Exporta un reporte semanal en formato Excel.
- **Servicio de Aplicación:** `generar_reporte_semanal_excel`

### `GET /api/reportes/export/mensual/`

- **Descripción:** Exporta un reporte mensual en formato Excel.
- **Servicio de Aplicación:** `generar_reporte_mensual_excel`

## 4. Requisitos y Configuración

- **Dependencias:** Django, djangorestframework, openpyxl, asyncpg.
- **Variables de Entorno:** `DATABASE_URL` para la conexión a la base de datos.

## 5. Buenas Prácticas y Estándares

- **Asincronismo:** Los servicios de aplicación son asíncronos para manejar operaciones de base de datos de manera eficiente.
- **Fallback:** Los servicios tienen un mecanismo de fallback para devolver una respuesta válida incluso si la base de datos no está disponible.
- **Serializers:** Aunque no se usan serializers de DRF, se utilizan funciones de serialización para convertir los datos a un formato JSON adecuado.
