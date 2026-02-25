import { useState, useMemo } from "react";
import {
  Users,
  UsersRound,
  UserCheck,
  GraduationCap,
  FileCheck,
  FileX,
  UserX,
  Clock,
  Info,
  AlertTriangle,
  AlertOctagon,
  ShieldAlert,
  Bell,
  Activity,
  Search,
  Filter
} from "lucide-react";
import './PuntualidadDashboard.css';
import Justificaciones from './Justificaciones';
import Recuperacion from './Recuperacion';

// Datos de ejemplo para los practicantes
const practicantesEjemplo = [
  {
    id: 1,
    nombre: "Carlos Mendoza",
    servidor: "Rpsoft",
    equipo: "Team Alpha",
    estado: "Presente",
    horaIngreso: "8:02 a.m.",
    horasSemanales: "24/30",
    progreso: 85,
    colorProgreso: "#facc15",
    ticket: null,
    warning: null
  },
  {
    id: 2,
    nombre: "Ana Torres",
    servidor: "Innovacion",
    equipo: "Team Beta",
    estado: "Tardanza",
    horaIngreso: "8:12 a.m.",
    horasSemanales: "18/30",
    progreso: 70,
    colorProgreso: "#ef4444",
    ticket: null,
    warning: null
  },
  {
    id: 3,
    nombre: "María González",
    servidor: "Laboratorios",
    equipo: "Team Gamma",
    estado: "Ausente",
    horaIngreso: "—",
    horasSemanales: "12/30",
    progreso: 40,
    colorProgreso: "#ef4444",
    ticket: null,
    warning: null
  },
  {
    id: 4,
    nombre: "Pedro Sánchez",
    servidor: "MiniBootcamp",
    equipo: "Team Delta",
    estado: "Ausente (Justificado)",
    horaIngreso: "—",
    horasSemanales: "18/30",
    progreso: 60,
    colorProgreso: "#ef4444",
    ticket: "Ticket #1234 – Cita médica",
    warning: null
  },
  {
    id: 5,
    nombre: "Luis Ramírez",
    servidor: "Rpsoft",
    equipo: "Team Alpha",
    estado: "Presente",
    horaIngreso: "7:58 a.m.",
    horasSemanales: "30/30",
    progreso: 100,
    colorProgreso: "#16a34a",
    ticket: null,
    warning: "⚠ Sin Daily del equipo registrado hoy"
  },
  {
    id: 6,
    nombre: "Juan Pérez",
    servidor: "Recuperacion",
    equipo: "Team Epsilon",
    estado: "Tardanza",
    horaIngreso: "8:10 a.m.",
    horasSemanales: "20/30",
    progreso: 67,
    colorProgreso: "#ef4444",
    ticket: null,
    warning: null
  },
  {
    id: 7,
    nombre: "Laura Gómez",
    servidor: "Innovacion",
    equipo: "Team Beta",
    estado: "Presente",
    horaIngreso: "7:55 a.m.",
    horasSemanales: "28/30",
    progreso: 93,
    colorProgreso: "#16a34a",
    ticket: null,
    warning: null
  },
  {
    id: 8,
    nombre: "Roberto Castro",
    servidor: "Laboratorios",
    equipo: "Team Gamma",
    estado: "Presente",
    horaIngreso: "8:00 a.m.",
    horasSemanales: "25/30",
    progreso: 83,
    colorProgreso: "#facc15",
    ticket: null,
    warning: null
  },
  {
    id: 9,
    nombre: "Sofía Rodríguez",
    servidor: "MiniBootcamp",
    equipo: "Team Delta",
    estado: "Tardanza",
    horaIngreso: "8:07 a.m.",
    horasSemanales: "22/30",
    progreso: 73,
    colorProgreso: "#ef4444",
    ticket: null,
    warning: null
  },
  {
    id: 10,
    nombre: "Miguel Ángel",
    servidor: "Recuperacion",
    equipo: "Team Epsilon",
    estado: "Ausente (Justificado)",
    horaIngreso: "—",
    horasSemanales: "15/30",
    progreso: 50,
    colorProgreso: "#ef4444",
    ticket: "Ticket #1235 – Consulta médica",
    warning: null
  }
];

// Opciones para los filtros
const servidores = ["Todos los servidores", "Innovacion", "Rpsoft", "MiniBootcamp", "Laboratorios", "Recuperacion"];
const estados = ["Todos los estados", "Presente", "Tardanza", "Ausente", "Ausente (Justificado)"];

export default function App() {
  const [activeTab, setActiveTab] = useState("vista");
  const [busqueda, setBusqueda] = useState("");
  const [servidorFiltro, setServidorFiltro] = useState("Todos los servidores");
  const [estadoFiltro, setEstadoFiltro] = useState("Todos los estados");

  // Filtrar practicantes
  const practicantesFiltrados = useMemo(() => {
    return practicantesEjemplo.filter(practicante => {
      // Filtro por búsqueda de nombre
      const coincideNombre = busqueda === "" || 
        practicante.nombre.toLowerCase().includes(busqueda.toLowerCase());
      
      // Filtro por servidor
      const coincideServidor = servidorFiltro === "Todos los servidores" || 
        practicante.servidor === servidorFiltro;
      
      // Filtro por estado
      const coincideEstado = estadoFiltro === "Todos los estados" || 
        (estadoFiltro === "Ausente" ? 
          practicante.estado === "Ausente" : 
          practicante.estado === estadoFiltro);
      
      return coincideNombre && coincideServidor && coincideEstado;
    });
  }, [busqueda, servidorFiltro, estadoFiltro]);

  return (
    <div className="page">
      <header className="header">
        <h1>Puntualidad y Asistencia</h1>
        <p className="subtext">
          Control diario de asistencia con auto-exclusión y alertas automáticas
        </p>
      </header>

      {/* Tabs */}
      <div className="tabs">
        <button
          className={activeTab === "vista" ? "active" : ""}
          onClick={() => setActiveTab("vista")}
        >
          Vista Hoy
        </button>
        <button
          className={activeTab === "justificaciones" ? "active" : ""}
          onClick={() => setActiveTab("justificaciones")}
        >
          Justificaciones
        </button>
        <button
          className={activeTab === "recuperacion" ? "active" : ""}
          onClick={() => setActiveTab("recuperacion")}
        >
          Recuperación
        </button>
      </div>

      {activeTab === "vista" && (
        <>
          <div className="resume-header">
            <h2 className="resume-title">Resumen de Asistencia Hoy</h2>
            <div className="header-update">
              <span>
                Última actualización: <strong>7:45 a.m.</strong>
              </span>
            </div>
          </div>

          {/* === Resumen de Asistencia === */}
          <section className="grid-resume">
            <div className="card">
              <div className="card-content">
                <h3>Deben Asistir Hoy</h3>
                <div className="big">128</div>
                <p className="note">Excluye los que tienen clases</p>
              </div>
              <div className="card-icon blue"><UsersRound size={36} /></div>
            </div>

            <div className="card">
              <div className="card-content">
                <h3>Presentes</h3>
                <div className="big">118 <span className="small">(92%)</span></div>
                <p className="note">&nbsp;</p>
              </div>
              <div className="card-icon green"><UserCheck size={36} /></div>
            </div>

            <div className="card">
              <div className="card-content">
                <h3>Con Clases Hoy</h3>
                <div className="big">24</div>
                <p className="note">Auto-excluidos del registro</p>
              </div>
              <div className="card-icon purple"><GraduationCap size={36} /></div>
            </div>

            <div className="card">
              <div className="card-content">
                <h3>Ausentes Justificados</h3>
                <div className="big">6</div>
                <p className="note">Con ticket aprobado</p>
              </div>
              <div className="card-icon orange"><UserX size={36} /></div>
            </div>

            <div className="card">
              <div className="card-content">
                <h3>Ausentes Sin Justificar</h3>
                <div className="big">4</div>
                <p className="note">Requieren atención</p>
              </div>
              <div className="card-icon red"><AlertTriangle size={36} /></div>
            </div>

            <div className="card">
              <div className="card-content">
                <h3>Tardanzas</h3>
                <div className="big">8</div>
                <p className="note">Llegaron después de 8:05</p>
              </div>
              <div className="card-icon yellow"><Clock size={36} /></div>
            </div>
          </section>

          {/* === Autoexclusión === */}
          <div className="auto">
            <div className="auto-icon"><UsersRound size={22} /></div>
            <div>
              <h4>Auto-exclusión diaria activada</h4>
              <p>
                A las <strong>7:45 a.m.</strong> se generó automáticamente la lista de practicantes que deben asistir hoy,
                excluyendo a los 24 que tienen clases programadas en su calendario.
              </p>
            </div>
          </div>

          {/* === Alertas === */}
          <div className="alerts">
            <h2>Alertas Automáticas</h2>

            <div className="alerts-grid">
              <div className="alert yellow">
                <div className="alert-header">
                  <div className="alert-header-left">
                    <div className="icon-wrap yellow"><AlertTriangle size={20} /></div>
                    <h3>Tardanza potencial detectada</h3>
                  </div>
                  <div className="count">3</div>
                </div>
                <p className="time">8:05 a.m. • Gracia de 5 minutos aplicada</p>
                <ul>
                  <li>Carlos Mendoza</li>
                  <li>Ana Torres</li>
                  <li>Luis Ramírez</li>
                </ul>
                <button className="btn secondary">Ver detalles</button>
              </div>

              <div className="alert red">
                <div className="alert-header">
                  <div className="alert-header-left">
                    <div className="icon-wrap red"><AlertTriangle size={20} /></div>
                    <h3>Ausencias sin clase registrada</h3>
                  </div>
                  <div className="count">2</div>
                </div>
                <p className="time">8:30 a.m. • No tienen clases programadas hoy</p>
                <ul>
                  <li>María González</li>
                  <li>Pedro Sánchez</li>
                </ul>
                <button className="btn secondary">Ver detalles</button>
              </div>

              <div className="alert orange">
                <div className="alert-header">
                  <div className="alert-header-left">
                    <div className="icon-wrap orange"><ShieldAlert size={20} /></div>
                    <h3>Practicantes en riesgo</h3>
                  </div>
                  <div className="count">1</div>
                </div>
                <p className="time">9:15 a.m. • 3er ticket del mes alcanzado</p>
                <ul>
                  <li>Jorge Vega</li>
                </ul>
                <button className="btn secondary">Ver detalles</button>
              </div>
            </div>
          </div>

          {/* === Configuración === */}
          <div className="config">
            <div className="config-header">
              <Bell size={18} /> <h3>Configuración de alertas</h3>
            </div>
            <ul>
              <li>8:05 a.m. – Alerta de tardanza potencial (gracia 5 min)</li>
              <li>8:30 a.m. – Alerta de ausencia sin clase registrada</li>
              <li>3er ticket del mes – Alerta de practicante en riesgo</li>
              <li>Sin Daily del equipo – Bandera en asistencia (cruce automático)</li>
            </ul>
          </div>

          {/* ⭐⭐⭐ CONTROL DE ASISTENCIA DIARIA ⭐⭐⭐ */}
          <div className="control-diario">
            <h2>Control de Asistencia Diaria</h2>

            <div className="control-wrap">
              <div className="controls">
                <div className="search-box">
                  <Search size={18} />
                  <input 
                    type="text" 
                    placeholder="Buscar por nombre..." 
                    value={busqueda}
                    onChange={(e) => setBusqueda(e.target.value)}
                  />
                </div>

                <div className="filter-group">
                  <button className="filter-btn">
                    <Filter size={18} /> 
                    <select 
                      value={servidorFiltro}
                      onChange={(e) => setServidorFiltro(e.target.value)}
                      className="filter-select-inline"
                    >
                      {servidores.map(servidor => (
                        <option key={servidor} value={servidor}>
                          {servidor}
                        </option>
                      ))}
                    </select>
                  </button>

                  <select 
                    value={estadoFiltro}
                    onChange={(e) => setEstadoFiltro(e.target.value)}
                    className="state-select"
                  >
                    {estados.map(estado => (
                      <option key={estado} value={estado}>
                        {estado}
                      </option>
                    ))}
                  </select>
                </div>

                <span className="badge">{practicantesFiltrados.length} practicantes encontrados</span>
              </div>

              {/* === Lista === */}
              <div className="list">
                {practicantesFiltrados.map(practicante => (
                  <div key={practicante.id} className="person-card">
                    <div className="person-left">
                      <div className="person-name">
                        {practicante.nombre} <span className="tag">{practicante.servidor}</span> <span className="tag">{practicante.equipo}</span>
                      </div>
                      <div className="person-meta">
                        Hora de Ingreso: <strong>{practicante.horaIngreso}</strong> • Horas semanales: <strong>{practicante.horasSemanales}</strong>
                      </div>

                      <div className="progress">
                        <div 
                          className="progress-bar" 
                          style={{ 
                            width: `${practicante.progreso}%`, 
                            background: practicante.colorProgreso 
                          }}
                        ></div>
                      </div>

                      {practicante.ticket && (
                        <div className="warning">
                          {practicante.ticket}
                        </div>
                      )}

                      {practicante.warning && (
                        <div className="warning">
                          {practicante.warning}
                        </div>
                      )}
                    </div>

                    <div className="person-right">
                      <div className={`status ${
                        practicante.estado === "Presente" ? "present" : 
                        practicante.estado === "Tardanza" ? "tardanza" : 
                        practicante.estado.includes("Justificado") ? "ausenteJ" : 
                        "ausente"
                      }`}>
                        {practicante.estado}
                      </div>
                      <button className="btn secondary">Ver detalles</button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
          {/* ⭐⭐⭐ FIN DEL CONTROL DIARIO ⭐⭐⭐ */}

        </>
      )}

      {activeTab === "justificaciones" && <Justificaciones />}

      {activeTab === "recuperacion" && <Recuperacion />}
    </div>
  );
}