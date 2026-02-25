# apps/reportes/infrastructure/serializers.py

from datetime import date

def practicante_to_dict(p):
    if p is None:
        return None

    return {
        "id": p.id,
        "nombre": p.nombre,
        "apellido": p.apellido,
        "correo": p.correo,
        "semestre": p.semestre,
    }


def advertencia_mes_actual_to_dict(item):
    return {
        "practicante": practicante_to_dict(item.practicante),
        "cantidad_advertencias": item.cantidad_advertencias,
    }


def historial_advertencia_to_dict(item):
    return {
        "practicante": practicante_to_dict(item.practicante),
        "fecha": item.fecha,
        "motivo": item.motivo,
        "tipo": item.tipo,
    }


def detalle_cumplimiento_horas_to_dict(item):
    return {
        "practicante": practicante_to_dict(item.practicante),
        "horas_semanales": item.horas_semanales,
        "proyeccion_mensual": item.proyeccion_mensual,
        "porcentaje_meta": item.porcentaje_meta,
        "estado": item.estado,
    }


def resumen_global_horas_to_dict(data):
    return {
        "total_horas_trabajadas": data.total_horas_trabajadas,
        "meta_semanal_total": 240,
        "porcentaje_cumplimiento": data.porcentaje_cumplimiento,
        "practicantes_cumpliendo": data.practicantes_cumpliendo,
        "practicantes_criticos": data.practicantes_criticos,
        "total_practicantes": data.total_practicantes,
    }


def permiso_semana_to_dict(p):
    return {
        "id": p.id,
        "practicante": practicante_to_dict(p.practicante),
        "fecha_solicitud": p.fecha_solicitud,
        "motivo": p.motivo,
        "estado": p.estado,
    }


def resumen_permisos_practicante_to_dict(item):
    return {
        "practicante": practicante_to_dict(item.practicante),
        "aprobados": item.aprobados,
        "total_solicitados": item.total_solicitados,
    }


def dashboard_summary_to_dict(item):
    return {
        "total_horas": item.total_horas,
        "meta_semanal": 240,
        "cumplimiento_porcentaje": item.cumplimiento_porcentaje,
        "horas_faltantes": item.horas_faltantes,
    }
