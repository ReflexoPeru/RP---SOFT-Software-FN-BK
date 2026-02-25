import { useState } from "react";
import { Clock, CheckCircle, XCircle, AlertCircle } from "lucide-react";

export default function Justificaciones() {
  const [justifications, setJustifications] = useState([
    {
      id: "TKT-1234",
      practitioner: "Pedro Sánchez",
      server: "MiniBootcamp",
      date: "2025-01-06",
      reason: "Cita médica",
      status: "approved",
      submittedAt: "8:15 a.m.",
      reviewedAt: "9:30 a.m.",
      slaRemaining: null,
      monthlyCount: 2,
      recoveryPlan: {
        date: "2025-01-13",
        dayOfWeek: "Sábado",
        schedule: "8:00 AM - 2:00 PM",
        totalHours: 6,
        supervisor: "Juan Pérez",
        status: "pendiente"
      },
    },
    {
      id: "TKT-1235",
      practitioner: "María González",
      server: "Laboratorios",
      date: "2025-01-06",
      reason: "Emergencia familiar",
      status: "pending",
      submittedAt: "8:45 a.m.",
      reviewedAt: null,
      slaRemaining: "14h 15m",
      monthlyCount: 3,
    },
    {
      id: "TKT-1236",
      practitioner: "Jorge Vega",
      server: "Rpsoft",
      date: "2025-01-05",
      reason: "Trámite personal",
      status: "rejected",
      submittedAt: "9:00 a.m.",
      reviewedAt: "10:15 a.m.",
      slaRemaining: null,
      monthlyCount: 3,
      rejectionReason: "Sin evidencia adjunta",
    },
    {
      id: "TKT-1237",
      practitioner: "Ana Torres",
      server: "Innovacion",
      date: "2025-01-06",
      reason: "Problema de transporte",
      status: "expired",
      submittedAt: "Ayer 8:30 a.m.",
      reviewedAt: null,
      slaRemaining: "Vencido",
      monthlyCount: 1,
    },
    {
      id: "TKT-1238",
      practitioner: "Carlos Ramírez",
      server: "Desarrollo",
      date: "2025-01-07",
      reason: "Capacitación externa",
      status: "approved",
      submittedAt: "7:45 a.m.",
      reviewedAt: "10:20 a.m.",
      slaRemaining: null,
      monthlyCount: 1,
      recoveryPlan: {
        date: "2025-01-14",
        dayOfWeek: "Martes",
        schedule: "8:00 AM - 12:00 PM",
        totalHours: 4,
        supervisor: "Laura Martínez",
        status: "completado"
      },
    },
  ]);

  const getStatusConfig = (status) => {
    const configs = {
      approved: {
        label: "Aprobado",
        icon: CheckCircle,
        className: "status-approved",
      },
      pending: {
        label: "Pendiente",
        icon: Clock,
        className: "status-pending",
      },
      rejected: {
        label: "Rechazado",
        icon: XCircle,
        className: "status-rejected",
      },
      expired: {
        label: "Vencido",
        icon: AlertCircle,
        className: "status-expired",
      },
    };
    return configs[status];
  };

  const calculateRecoveryDate = (originalDate) => {
    const date = new Date(originalDate);
    
    // Intentamos encontrar un día de recuperación (lunes a sábado)
    for (let i = 7; i <= 14; i++) { // Buscamos entre 7 y 14 días después
      const recoveryDate = new Date(date);
      recoveryDate.setDate(recoveryDate.getDate() + i);
      const dayOfWeek = recoveryDate.getDay(); // 0 = Domingo, 1 = Lunes, ..., 6 = Sábado
      
      if (dayOfWeek >= 1 && dayOfWeek <= 6) { // Lunes(1) a Sábado(6)
        return recoveryDate;
      }
    }
    
    // Si no encontramos en ese rango, devolvemos 7 días después como fallback
    date.setDate(date.getDate() + 7);
    return date;
  };

  const handleApprove = (id) => {
    const ticket = justifications.find(t => t.id === id);
    if (ticket) {
      // Calcular fecha de recuperación evitando domingos
      const recoveryDate = calculateRecoveryDate(ticket.date);
      
      const daysOfWeek = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"];
      const dayOfWeek = daysOfWeek[recoveryDate.getDay()];
      
      // Determinar supervisor basado en el servidor
      const supervisors = {
        "MiniBootcamp": "Juan Pérez",
        "Laboratorios": "María López",
        "Rpsoft": "Carlos Gómez",
        "Innovacion": "Ana Rodríguez",
        "Desarrollo": "Laura Martínez",
        "Tu servidor": "Supervisor asignado"
      };
      
      // Horario estándar para recuperaciones
      const recoverySchedule = "8:00 AM - 2:00 PM";
      const totalHours = 6;
      
      // Si cae en sábado, puede ser horario completo
      if (recoveryDate.getDay() === 6) { // Sábado
        recoverySchedule = "8:00 AM - 2:00 PM";
        totalHours = 6;
      }
      
      const recoveryPlan = {
        date: recoveryDate.toISOString().split('T')[0],
        dayOfWeek: dayOfWeek,
        schedule: recoverySchedule,
        totalHours: totalHours,
        supervisor: supervisors[ticket.server] || "Supervisor por asignar",
        status: "pendiente"
      };

      setJustifications(justifications.map(ticket => 
        ticket.id === id 
          ? { 
              ...ticket, 
              status: "approved", 
              reviewedAt: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
              slaRemaining: null,
              recoveryPlan: recoveryPlan
            }
          : ticket
      ));
    }
  };

  const handleReject = (id) => {
    const rejectionReason = prompt("Ingrese el motivo del rechazo:");
    if (rejectionReason) {
      setJustifications(justifications.map(ticket => 
        ticket.id === id 
          ? { 
              ...ticket, 
              status: "rejected", 
              reviewedAt: new Date().toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' }),
              rejectionReason,
              slaRemaining: null 
            }
          : ticket
      ));
    }
  };

  return (
    <div className="justifications-container">
      <div className="justifications-header">
        <h2>Gestión de Justificaciones</h2>
      </div>

      <div className="info-card sla-info">
        <div className="info-icon">
          <Clock size={20} />
        </div>
        <div className="info-content">
          <p className="info-title">SLA de tickets: ≤24 horas</p>
          <p className="info-text">
            Los tickets deben ser revisados en máximo 24 horas. Si vencen sin evidencia adjunta, se rechazan
            automáticamente. Límite: <strong>3 tickets por mes</strong>. 
            <br />Horario de recuperación estándar: <strong>8:00 AM - 2:00 PM</strong>
            <br /><strong>Nota:</strong> Las recuperaciones solo se programan de <strong>Lunes a Sábado</strong>. 
            Los domingos no hay recuperación.
          </p>
        </div>
      </div>

      <div className="justifications-list">
        {justifications.map((ticket) => {
          const statusConfig = getStatusConfig(ticket.status);
          const StatusIcon = statusConfig.icon;
          const isAtLimit = ticket.monthlyCount >= 3;

          return (
            <div key={ticket.id} className="justification-card">
              <div className="justification-content">
                <div className="justification-header-row">
                  <h3>{ticket.practitioner}</h3>
                  <span className="badge-outline">{ticket.server}</span>
                  <span className="badge-outline">{ticket.id}</span>
                  {isAtLimit && (
                    <span className="badge-danger">
                      <AlertCircle size={12} />
                      Límite alcanzado
                    </span>
                  )}
                </div>

                <div className="justification-details">
                  <p><strong>Motivo:</strong> {ticket.reason}</p>
                  <p><strong>Fecha:</strong> {ticket.date}</p>
                  <p><strong>Enviado:</strong> {ticket.submittedAt}</p>
                  {ticket.reviewedAt && (
                    <p><strong>Revisado:</strong> {ticket.reviewedAt}</p>
                  )}
                  {ticket.rejectionReason && (
                    <p className="rejection-reason">
                      <strong>Motivo de rechazo:</strong> {ticket.rejectionReason}
                    </p>
                  )}
                  {ticket.recoveryPlan && (
                    <div className="recovery-info">
                      <p><strong>Recuperación programada:</strong></p>
                      <p>{ticket.recoveryPlan.dayOfWeek}, {ticket.recoveryPlan.date}</p>
                      <p>{ticket.recoveryPlan.schedule} ({ticket.recoveryPlan.totalHours} horas)</p>
                      <p><strong>Supervisor:</strong> {ticket.recoveryPlan.supervisor}</p>
                    </div>
                  )}
                </div>

                <div className="justification-badges">
                  <span className="badge-outline">
                    {ticket.monthlyCount}/3 tickets este mes
                  </span>
                </div>

                {ticket.slaRemaining && ticket.status === "pending" && (
                  <div className="sla-warning">
                    <Clock size={14} />
                    <span>SLA: {ticket.slaRemaining} restantes</span>
                  </div>
                )}
              </div>

              <div className="justification-actions">
                <span className={`status-badge ${statusConfig.className}`}>
                  <StatusIcon size={14} />
                  {statusConfig.label}
                </span>
                {ticket.status === "pending" && (
                  <div className="action-buttons">
                    <button className="btn-approve" onClick={() => handleApprove(ticket.id)}>
                      Aprobar
                    </button>
                    <button className="btn-reject" onClick={() => handleReject(ticket.id)}>
                      Rechazar
                    </button>
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      <style jsx>{`
        .justifications-container {
          padding: 20px;
          max-width: 1200px;
          margin: 0 auto;
        }

        .justifications-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
        }

        .justifications-header h2 {
          margin: 0;
          font-size: 24px;
          color: #333;
        }

        .btn-primary {
          background: #3b82f6;
          color: white;
          border: none;
          padding: 10px 20px;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .btn-primary:hover {
          background: #2563eb;
        }

        .btn-secondary {
          background: #f3f4f6;
          color: #374151;
          border: 1px solid #d1d5db;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .btn-secondary:hover {
          background: #e5e7eb;
        }

        .btn-approve {
          background: #10b981;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
        }

        .btn-reject {
          background: #ef4444;
          color: white;
          border: none;
          padding: 8px 16px;
          border-radius: 6px;
          cursor: pointer;
          font-weight: 500;
        }

        .btn-approve:hover {
          background: #059669;
        }

        .btn-reject:hover {
          background: #dc2626;
        }

        .info-card {
          background: #f0f9ff;
          border: 1px solid #bae6fd;
          border-radius: 8px;
          padding: 16px;
          margin-bottom: 24px;
          display: flex;
          gap: 12px;
          align-items: flex-start;
        }

        .info-icon {
          color: #0284c7;
        }

        .info-title {
          font-weight: 600;
          margin: 0 0 4px 0;
          color: #0369a1;
        }

        .info-text {
          margin: 0;
          color: #475569;
          font-size: 14px;
        }

        .justification-card {
          background: white;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 20px;
          margin-bottom: 16px;
          display: flex;
          justify-content: space-between;
          gap: 20px;
        }

        .justification-header-row {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
          flex-wrap: wrap;
        }

        .justification-header-row h3 {
          margin: 0;
          font-size: 18px;
          color: #111827;
        }

        .badge-outline {
          border: 1px solid #d1d5db;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          color: #6b7280;
        }

        .badge-danger {
          background: #fee2e2;
          color: #dc2626;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .badge-success {
          background: #d1fae5;
          color: #059669;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .badge-gray {
          background: #f3f4f6;
          color: #6b7280;
          padding: 4px 8px;
          border-radius: 4px;
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 4px;
        }

        .justification-details {
          margin-bottom: 12px;
        }

        .justification-details p {
          margin: 4px 0;
          font-size: 14px;
          color: #4b5563;
        }

        .recovery-info {
          background: #f0f9ff;
          padding: 12px;
          border-radius: 6px;
          border-left: 4px solid #0284c7;
          margin-top: 8px;
          color: #0369a1 !important;
        }

        .recovery-info p {
          margin: 4px 0 !important;
          color: #0369a1 !important;
        }

        .rejection-reason {
          color: #dc2626 !important;
          font-weight: 500;
        }

        .justification-badges {
          display: flex;
          gap: 8px;
          margin-bottom: 12px;
        }

        .status-badge {
          padding: 6px 12px;
          border-radius: 20px;
          font-size: 12px;
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .status-approved {
          background: #d1fae5;
          color: #059669;
        }

        .status-pending {
          background: #fef3c7;
          color: #d97706;
        }

        .status-rejected {
          background: #fee2e2;
          color: #dc2626;
        }

        .status-expired {
          background: #e5e7eb;
          color: #6b7280;
        }

        .status-info {
          background: #dbeafe;
          color: #1d4ed8;
        }

        .status-gray {
          background: #f3f4f6;
          color: #6b7280;
        }

        .sla-warning {
          display: flex;
          align-items: center;
          gap: 6px;
          color: #d97706;
          font-size: 12px;
          margin-top: 8px;
        }

        .justification-actions {
          display: flex;
          flex-direction: column;
          gap: 12px;
          align-items: flex-end;
          min-width: 200px;
        }

        .action-buttons {
          display: flex;
          gap: 8px;
        }
      `}</style>
    </div>
  );
}