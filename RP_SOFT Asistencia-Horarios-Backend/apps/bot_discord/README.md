# Módulo: Bot de Discord

## 1. Descripción del Módulo

Este módulo es responsable de gestionar y monitorear el estado de un bot de Discord, así como de recopilar y exponer métricas sobre su rendimiento y actividad en los servidores a los que está conectado.

- **Responsabilidad principal:** Recibir, almacenar y servir métricas y el estado de un bot de Discord.
- **Relación con otros módulos:** Actualmente, este módulo es independiente y no tiene dependencias directas con otros módulos de la aplicación.
- **Arquitectura Hexagonal:**
    - **Dominio:** Contiene las entidades (`MetricasGlobalesBot`, `EstadoBot`, `ServidoresBot`) y los repositorios que definen el contrato para la persistencia de datos.
    - **Aplicación:** Orquesta los casos de uso, como guardar métricas, obtener el estado del bot y listar servidores.
    - **Infraestructura:** Implementa los detalles técnicos, como los endpoints de la API (vistas de DRF), la persistencia de datos (Django ORM), los serializers y la comunicación en tiempo real (WebSockets con Django Channels).

## 2. Documentación de Endpoints

### Endpoint: `POST /api/bot/metrics/`

- **Método HTTP:** `POST`
- **Ruta completa:** `/api/bot/metrics/`
- **Use Case o Port que activa:** `GuardarMetricasBotService`
- **Descripción funcional:** Recibe y almacena un conjunto completo de métricas del bot de Discord, incluyendo un resumen global, el estado actual y una lista de servidores.
- **Parámetros:**
    - `body`: Un objeto JSON con la estructura definida en el `MetricasPayloadSerializer`.
- **Ejemplo de request:**
  ```json
  {
    "resumen": {
      "servidores_conectados": 10,
      "eventos_procesados_hoy": 500,
      "uptime_porcentaje": 99.9,
      "ultima_sincronizacion": "2023-10-27T10:00:00Z"
    },
    "estado": {
      "status": "online",
      "uptime_dias": 30,
      "latencia_ms": 120.5,
      "ultima_conexion": "2023-10-27T10:00:00Z"
    },
    "servers": [
      {
        "server_id": 12345,
        "server_name": "Servidor de Prueba",
        "miembros": 150,
        "canales": 20,
        "status": "conectado"
      }
    ]
  }
  ```
- **Ejemplo de response:**
  ```json
  {
    "message": "Métricas recibidas y emitidas"
  }
  ```
- **Códigos de estado posibles:**
    - `200 OK`: Métricas recibidas correctamente.
    - `400 Bad Request`: Datos de entrada inválidos.
    - `403 Forbidden`: Autenticación fallida.
- **Reglas de negocio:** El endpoint valida que el `status` del bot y de los servidores se encuentre entre los valores permitidos (`online`, `offline`, `maintenance` para el bot; `conectado`, `desconectado` para los servidores).
- **Requerimientos de autenticación/permisos:** Requiere autenticación basada en un token (`BOT_API_KEY`) en la cabecera `Authorization`.
- **Conexión con el Application Layer:** Invoca el servicio `GuardarMetricasBotService` para persistir las métricas recibidas.

### Endpoint: `POST /api/bot/status/`

- **Método HTTP:** `POST`
- **Ruta completa:** `/api/bot/status/`
- **Use Case o Port que activa:** `ActualizarEstadoBotService`
- **Descripción funcional:** Actualiza el estado del bot de Discord.
- **Parámetros:**
    - `body`: Un objeto JSON con el campo `status`.
- **Ejemplo de request:**
  ```json
  {
    "status": "offline"
  }
  ```
- **Ejemplo de response:**
  ```json
  {
    "message": "Estado del bot actualizado a offline"
  }
  ```
- **Códigos de estado posibles:**
    - `200 OK`: Estado actualizado correctamente.
    - `400 Bad Request`: `status` inválido.
    - `403 Forbidden`: Autenticación fallida.
- **Requerimientos de autenticación/permisos:** Requiere autenticación basada en un token (`BOT_API_KEY`).
- **Conexión con el Application Layer:** Invoca el servicio `ActualizarEstadoBotService`.

### Endpoint: `GET /api/bot/resumen/`

- **Método HTTP:** `GET`
- **Ruta completa:** `/api/bot/resumen/`
- **Use Case o Port que activa:** `ObtenerResumenGlobalService`
- **Descripción funcional:** Obtiene un resumen global de las métricas del bot.
- **Ejemplo de response:**
  ```json
  {
    "servidores_conectados": 10,
    "eventos_procesados_hoy": 500,
    "uptime_porcentaje": 99.9,
    "ultima_sincronizacion": "2023-10-27T10:00:00Z"
  }
  ```
- **Códigos de estado posibles:**
    - `200 OK`
    - `404 Not Found`: No hay datos de resumen disponibles.
- **Conexión con el Application Layer:** Invoca `ObtenerResumenGlobalService`.

### Endpoint: `GET /api/bot/estado/`

- **Método HTTP:** `GET`
- **Ruta completa:** `/api/bot/estado/`
- **Use Case o Port que activa:** `ObtenerEstadoBotService`
- **Descripción funcional:** Obtiene el estado actual del bot.
- **Ejemplo de response:**
  ```json
  {
    "status": "online",
    "uptime_dias": 30,
    "latencia_ms": 120.5,
    "ultima_conexion": "2023-10-27T10:00:00Z"
  }
  ```
- **Códigos de estado posibles:**
    - `200 OK`
    - `404 Not Found`: No hay datos de estado disponibles.
- **Conexión con el Application Layer:** Invoca `ObtenerEstadoBotService`.

### Endpoint: `GET /api/bot/servers/`

- **Método HTTP:** `GET`
- **Ruta completa:** `/api/bot/servers/`
- **Use Case o Port que activa:** `ListarServidoresService`
- **Descripción funcional:** Obtiene una lista de los servidores a los que el bot está conectado.
- **Ejemplo de response:**
  ```json
  [
    {
      "server_id": 12345,
      "server_name": "Servidor de Prueba",
      "miembros": 150,
      "canales": 20,
      "status": "conectado",
      "ultima_actualizacion": "2023-10-27T10:00:00Z"
    }
  ]
  ```
- **Códigos de estado posibles:**
    - `200 OK`
- **Conexión con el Application Layer:** Invoca `ListarServidoresService`.

## 3. WebSockets

### Endpoint: `ws/bot/metrics/`

- **Descripción:** Este endpoint de WebSocket permite a los clientes recibir actualizaciones en tiempo real de las métricas del bot.
- **Evento:** `metricas_update`
- **Payload del evento:** El mismo que el `MetricasPayloadSerializer` o una actualización parcial del estado.
- **Ejemplo de consumo (JavaScript):**
  ```javascript
  const socket = new WebSocket('ws://' + window.location.host + '/ws/bot/metrics/');

  socket.onmessage = function(e) {
      const data = JSON.parse(e.data);
      console.log('Nuevas métricas recibidas:', data);
  };

  socket.onclose = function(e) {
      console.error('Socket cerrado inesperadamente');
  };
  ```

## 4. Requisitos y Configuración

- **Variables de entorno:**
    - `BOT_API_KEY`: Token de autenticación para los endpoints que lo requieren.
- **Migraciones requeridas:** Se deben aplicar las migraciones del módulo para crear las tablas de la base de datos.
- **Dependencias del módulo:**
    - `django`
    - `djangorestframework`
    - `channels`
- **Consideraciones para testing:**
    - Utilizar `APIClient` de DRF para simular peticiones a los endpoints.
    - Mockear los repositorios en las pruebas de los servicios de aplicación para aislar la lógica de negocio.

## 5. Buenas Prácticas y Estándares

- **Convenciones de nombres:**
    - **Use Cases/Services:** `NombreAccionService` (ej. `GuardarMetricasBotService`).
    - **Ports/Repositories:** `NombreEntidadRepository` (ej. `BotMetricasRepository`).
    - **Serializers:** `NombrePayloadSerializer` (ej. `MetricasPayloadSerializer`).
- **Cómo extender el módulo:**
    - **Nuevos casos de uso:** Crear nuevos servicios en la capa de aplicación.
    - **Nuevas entidades de dominio:** Definir nuevas dataclasses en `domain/entities.py` y sus correspondientes repositorios.
    - **Nuevos endpoints:** Añadir nuevas vistas en `infrastructure/views.py` y sus rutas en `infrastructure/urls.py`.
- **Desacoplamiento del ORM:** El dominio está desacoplado del ORM de Django. Los servicios de aplicación dependen de las abstracciones de los repositorios, no de las implementaciones concretas.
