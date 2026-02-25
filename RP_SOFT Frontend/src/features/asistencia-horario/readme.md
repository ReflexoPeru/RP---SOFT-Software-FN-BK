

# 📌 Feature: `asistencia-horario`

Feature de RP Soft encargado de **asistencia, horarios, puntualidad, reportes, practicantes y seguimiento disciplinario**, con estructura modular (feature-based) y submódulos por dominio.

---

## 🧭 Responsabilidad del Feature

Este feature concentra pantallas y componentes para:

* Dashboard general del feature
* Integración con el bot (módulo “bot_integracion”)
* Control y resumen de asistencias (entradas/salidas, historial, justificaciones)
* Gestión de horarios (calendario semanal, aprobaciones, asignación)
* Historial de practicantes (resúmenes y detalle)
* Puntualidad y justificaciones
* Reportes (horas trabajadas, cumplimiento, advertencias, permisos)
* Seguimiento disciplinario (eventos semanales, secciones, agrupaciones)

---

## 🏗️ Estructura completa de carpetas

```
asistencia-horario/
├── index.jsx
├── README.md
├── .gitkeep
│
├── components/
│   ├── .gitkeep
│   ├── Layout/
│   │   ├── Layout.jsx
│   │   └── index.js
│   └── Sidebar/
│       ├── Sidebar.jsx
│       ├── Sidebar.module.css
│       ├── SidebarBackButton.jsx
│       ├── SidebarBackButton.module.css
│       └── index.js
│
├── hooks/
│   └── .gitkeep
│
├── pages/
│   ├── .gitkeep
│   ├── Dashboard.jsx
│   └── index.js
│
├── routes/
│   ├── .gitkeep
│   ├── router.jsx
│   └── index.js
│
├── services/
│   └── .gitkeep
│
├── store/
│   └── .gitkeep
│
└── modules/
    ├── bot_integracion/
    ├── control-asistencias/
    ├── gestion-horarios/
    ├── historial-practicantes/
    ├── inicio/
    ├── practicantes/
    ├── puntualidad/
    ├── reportes/
    └── seguimiento-disciplinario/
```

---

## 🧩 Estructura base del Feature

### `index.jsx`

Punto de entrada del feature.

* Exporta el componente principal que se monta desde el router general del sistema.
* Permite lazy-loading del feature.

### `components/Layout/Layout.jsx`

Layout contenedor del feature:

* Estructura general (sidebar + contenido)
* Reutilizable para todas las páginas/módulos internos.

### `components/Sidebar/`

Sidebar de navegación del feature:

* `Sidebar.jsx`: menú de navegación.
* `SidebarBackButton.jsx`: botón de regreso (UX).
* `*.module.css`: estilos encapsulados (CSS Modules).

### `pages/Dashboard.jsx`

Dashboard base del feature:

* Pantalla principal o resumen inicial (según rutas).
* Normalmente “entrada” visual antes de navegar a módulos.

### `routes/router.jsx`

Router interno del feature:

* Define rutas para páginas y módulos.
* Controla navegación interna sin depender del router global.

### `services/` y `store/`

Capas preparadas para:

* `services`: llamadas a API (Axios/Fetch) por dominio.
* `store`: estado global del feature (Redux/Zustand/Context), aún “placeholder”.

---

# ✅ MÓDULOS (`modules/`) — explicación completa

La carpeta `modules` contiene **subdominios funcionales**. Cada módulo agrupa:

* `pages/`: pantallas del módulo
* `components/`: componentes propios del módulo
* `hooks/`, `services/`, `store/`: capas opcionales por módulo (en algunos ya existe la estructura)

---

## 1) `modules/bot_integracion/`

**Propósito:** Pantalla de integración/monitoreo del bot.

**Contenido real:**

* `pages/Botintegrative.jsx`
* `pages/Botintegrative.module.css`

**Qué hace:**

* Renderiza la vista de integración del bot (UI).
* Estilos encapsulados.

---

## 2) `modules/control-asistencias/`

**Propósito:** Control y seguimiento directo de asistencias (historial, resumen, justificaciones).

**Contenido real:**

* `pages/ControlAsistencia.jsx` (+ CSS)
* Componentes:

  * `HistorialAsistencia/` (componente + estilos + index)
  * `JustificacionesEnviadas/` (componente + estilos + index)
  * `ResumenAsistencia/` (componente + estilos + index)
  * Además existen `HistorialAsistencia.jsx` y `ResumenAsistencia.jsx` a nivel de `components/` (wrappers o versiones directas).

**Qué hace:**

* Consolida UI para:

  * ver historial de asistencias
  * revisar resumen
  * visualizar justificaciones enviadas

---

## 3) `modules/gestion-horarios/`

**Propósito:** Gestión de horarios (agenda semanal, filtros, aprobaciones, asignación).

**Contenido real:**

* `pages/Dashboard.jsx` (+ CSS) y `pages/index.js`
* `components/`:

  * `AddScheduleDialog/` (dialog para agregar horario)
  * `CalendarWeekView/` (vista semanal tipo calendario)
  * `FilterBar/` (barra de filtros)
  * `PractitionersScheduleList/` (lista de horarios por practicante)
  * `ScheduleApprovalPanel/` (panel de aprobaciones)
  * `StatsCards/` (tarjetas de métricas)
  * `components/index.js` (export central)
* `hooks/`, `services/`, `store/` con `.gitkeep` (listos para crecer)

**Qué hace:**

* UI completa para gestionar horarios:

  * crear/asignar
  * filtrar
  * ver calendario semanal
  * aprobar horarios
  * visualizar métricas

---

## 4) `modules/historial-practicantes/`

**Propósito:** Historial consolidado por practicante, con filtros y tablas.

**Contenido real:**

* `pages/HistorialPracticantes.jsx` (+ CSS)
* `components/`:

  * `EstadisticasCards.jsx`
  * `EstadisticasResumen/` (+ CSS)
  * `FiltrosHistorial/` (+ CSS)
  * `TablaHistorialDetallado/` (+ CSS)
  * `TablaResumenPracticante/` (+ CSS)

**Qué hace:**

* Permite:

  * filtrar historiales
  * ver resúmenes por practicante
  * ver detalle tabular completo
  * mostrar estadísticas del historial

---

## 5) `modules/inicio/`

**Propósito:** Componentes “home” / inicio del feature (tarjetas informativas, alertas, stats).

**Contenido real:**

* `components/`:

  * `InfAlertCard/` (+ CSS + index)
  * `InfCards/` (+ CSS + index)
  * `StatsCards/` (+ CSS + index)
* `pages/`:

  * `Dashboard.module.css`
  * `nicolayus.jsx` (vista/página del módulo)

**Qué hace:**

* Renderiza tarjetas informativas y alertas del inicio.
* Sirve como vista de bienvenida/resumen.

---

## 6) `modules/practicantes/`

**Propósito:** Gestión y visualización de practicantes (dashboard, perfil, filtros, cards, stats).

**Contenido real:**

* `pages/`:

  * `Dashboard.jsx` (+ CSS)
  * `PerfilPracticante.jsx` (+ CSS)
  * `pages/index.js`
* `components/`:

  * `PracticanteCard/` (+ CSS + index)
  * `SearchAndFilters/` (+ CSS + index)
  * `StatsCards/` (+ CSS + index)
  * `components/index.js`
* `hooks/`, `services/`, `store/` con `.gitkeep`

**Qué hace:**

* Listado/visualización de practicantes con filtros.
* Perfil detallado por practicante.
* Métricas en tarjetas.

---

## 7) `modules/puntualidad/`

**Propósito:** Puntualidad, justificaciones y recuperación (vistas y componentes de control).

**Contenido real:**

* `pages/`:

  * `PuntualidadDashboard.jsx`
  * `PuntualidadDashboard.css`
  * `Justificaciones.jsx`
  * `Recuperacion.jsx`
  * `pages/index.js`
* `components/`:

  * `AlertCard/AlertCard.jsx`
  * `AlertCards/` (+ CSS + index)
  * `Card/Card.jsx`
  * `ControlAsistencia/` (+ CSS + index)
  * `ControlList/ControlList.jsx`
  * `Modal/Modal.jsx`
* `index.js` (export del módulo)
* `hooks/`, `services/`, `store/` con `.gitkeep`

**Qué hace:**

* Dashboard de puntualidad.
* Gestión de justificaciones.
* Pantalla de recuperación.
* Componentes de alertas, listas y modales.

---

## 8) `modules/reportes/`

**Propósito:** Reportes y métricas (horas trabajadas, cumplimiento, advertencias, permisos).

**Contenido real:**

* `pages/Reports.jsx` (+ CSS)
* `components/`:

  * `HoursWorked/`:

    * `HoursWorked.jsx` (+ CSS)
    * `ComplianceSummary.jsx` (+ CSS)
    * `HourDetail.jsx` (+ CSS)
  * `Permissions/Permissions.jsx` (+ CSS)
  * `StatsCardReports/ReportsCards.jsx` (+ CSS)
  * `Warning/ContentWarnings.jsx` (+ CSS)

**Qué hace:**

* Consolida reportes operativos:

  * horas trabajadas
  * cumplimiento/resumen
  * advertencias de contenido
  * permisos
  * tarjetas de reportes

---

## 9) `modules/seguimiento-disciplinario/`

**Propósito:** Seguimiento disciplinario por semanas/eventos (estructura tipo “timeline semanal”).

**Contenido real:**

* `pages/DisciplinaryTrackingView.jsx` (+ CSS)
* `components/`:

  * `ClassCard/` (+ CSS)
  * `SectionCard/` (+ CSS)
  * `WeekEventRow/` (+ CSS)
  * `WeekListGroup/` (+ CSS)

**Qué hace:**

* Página principal que orquesta el seguimiento.
* Componentes para:

  * tarjetas por clase/sección
  * filas de eventos por día
  * agrupaciones por semana

---

## 🔁 Flujo de navegación típico (resumen)

1. Se monta `asistencia-horario` desde `index.jsx`
2. `Layout` arma el contenedor del feature
3. `Sidebar` navega entre módulos
4. `routes/router.jsx` decide qué `page` o `module page` renderizar
5. Cada módulo usa sus componentes internos y estilos CSS Modules

---