# app/infrastructure/serializers.py

def practicante_to_dict(p):
    return {
        "id": getattr(p, "id", None),
        "nombre": f"{getattr(p, 'nombre', '')} {getattr(p, 'apellido', '')}".strip(),
        "servidor": getattr(p, "servidor", None) or "Sin asignar",
        "horario_completo": len(getattr(p, "horarios", [])) >= 5
    }


def horario_to_dict(horarios):
    if isinstance(horarios, list):
        return [{"id": h.get("id"), "dia": h.get("dia")} for h in horarios]
    return []


def recuperacion_to_dict(r):
    practicante = getattr(r, "practicante", None)

    nombre_practicante = ""
    if practicante:
        nombre_practicante = f"{getattr(practicante, 'nombre', '')} {getattr(practicante, 'apellido', '')}".strip()

    return {
        "id": getattr(r, "id", None),
        "practicante": nombre_practicante,
        "fecha_declarada": getattr(r, "fecha_recuperacion", None),
        "motivo": getattr(r, "motivo", None) or "Sin motivo",
        "evidencia_url": f"/media/{getattr(r, 'evidencia', '')}"
    }
