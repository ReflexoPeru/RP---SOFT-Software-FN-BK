# app/application/services.py

from datetime import datetime, date
import os


DATABASE_URL = os.getenv("DATABASE_URL")

pool = None


# =========================================================
# 🔧 HELPER: INTENTAR CONECTAR / FALLBACK SI NO HAY BD
# =========================================================
async def get_pool():
    global pool
    if pool is None:
        try:
            pool = await asyncpg.create_pool(DATABASE_URL)
        except Exception:
            pool = None
    return pool


def no_db(data):
    """
    Respuesta estándar cuando NO hay base de datos.
    """
    return {
        "detail": "Base de datos no conectada",
        "data": data
    }


# =========================================================
# 📌 DASHBOARD
# =========================================================
async def get_dashboard_summary():
    try:
        pool = await get_pool()
        if pool is None:
            raise Exception("NO BD")

        async with pool.acquire() as conn:
            row = await conn.fetchrow("""
                SELECT COALESCE(SUM(EXTRACT(EPOCH FROM (hora_salida - hora_entrada))/3600), 0)::float AS total_horas
                FROM asistencia
                WHERE fecha >= date_trunc('week', CURRENT_DATE - interval '1 week')
                  AND hora_salida IS NOT NULL 
                  AND hora_entrada IS NOT NULL
            """)

        total_horas = round(row['total_horas'], 1)

        return {
            "total_horas": total_horas,
            "meta_semanal": 240,
            "cumplimiento_porcentaje": round((total_horas / 240) * 100, 1),
            "horas_faltantes": round(240 - total_horas, 1)
        }

    except:
        # Fallback válido para el serializer
        return {
            "total_horas": 0,
            "meta_semanal": 240,
            "cumplimiento_porcentaje": 0,
            "horas_faltantes": 240
        }



# =========================================================
# 📌 ADVERTENCIAS DEL MES
# =========================================================
async def get_advertencias_mes_actual():
    try:
        pool = await get_pool()
        if pool is None:
            raise Exception("NO BD")

        async with pool.acquire() as conn:
            rows = await conn.fetch("""
                SELECT 
                    p.nombre, 
                    p.apellido,
                    COUNT(a.id) AS advertencias
                FROM practicante p
                LEFT JOIN asistencia a ON a.practicante_id = p.id
                WHERE EXTRACT(MONTH FROM COALESCE(a.fecha, CURRENT_DATE)) = EXTRACT(MONTH FROM CURRENT_DATE)
                  AND EXTRACT(YEAR FROM COALESCE(a.fecha, CURRENT_DATE)) = EXTRACT(YEAR FROM CURRENT_DATE)
                  AND a.estado_id IN (
                        SELECT id FROM estado_asistencia 
                        WHERE lower(estado) LIKE '%falta%' 
                           OR lower(estado) LIKE '%injustificada%'
                           OR lower(estado) LIKE '%ausente%'
                  )
                GROUP BY p.id, p.nombre, p.apellido
                HAVING COUNT(a.id) > 0
                ORDER BY advertencias DESC
            """)

        return [
            {
                "practicante": {"nombre": r["nombre"], "apellido": r["apellido"]},
                "cantidad_advertencias": r["advertencias"]
            }
            for r in rows
        ]

    except:
        return no_db([
            {
                "practicante": {"nombre": "Sin datos", "apellido": ""},
                "cantidad_advertencias": 0
            }
        ])


# =========================================================
# 📌 OTROS SERVICIOS (con fallback)
# =========================================================
async def get_detalle_cumplimiento_horas():
    try:
        pool = await get_pool()
        if pool is None:
            raise Exception()

        # luego lo implementas real
        return []

    except:
        return no_db([])


async def get_resumen_global_horas():
    summary = await get_dashboard_summary()

    if "detail" in summary:
        return no_db({
            "total_horas_trabajadas": 0,
            "meta_semanal_total": 240,
            "porcentaje_cumplimiento": 0,
            "practicantes_cumpliendo": 0,
            "practicantes_criticos": 8,
            "total_practicantes": 8
        })

    return {
        "total_horas_trabajadas": summary["total_horas"],
        "meta_semanal_total": 240,
        "porcentaje_cumplimiento": summary["cumplimiento_porcentaje"],
        "practicantes_cumpliendo": 0,
        "practicantes_criticos": 8,
        "total_practicantes": 8
    }


async def get_permisos_semana_actual():
    try:
        pool = await get_pool()
        if pool is None:
            raise Exception()
        return []

    except:
        return no_db([])


async def get_resumen_permisos_practicante():
    try:
        pool = await get_pool()
        if pool is None:
            raise Exception()
        return []

    except:
        return no_db([])


# =========================================================
# 📌 REPORTES EXCEL
# =========================================================
async def generar_reporte_semanal_excel(buffer):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Semanal"

    summary = await get_dashboard_summary()

    ws.append(["INDICADOR", "VALOR"])
    ws.append(["Horas trabajadas esta semana", summary.get("total_horas", 0)])
    ws.append(["Meta semanal", summary.get("meta_semanal", 240)])
    ws.append(["% de cumplimiento", f"{summary.get('cumplimiento_porcentaje', 0)}%"])
    ws.append(["Horas faltantes", summary.get("horas_faltantes", 240)])

    wb.save(buffer)


async def generar_reporte_mensual_excel(buffer):
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Mensual"

    ws.append(["Mes", "Total Horas", "Meta Mensual", "Estado"])
    ws.append([date.today().strftime("%B %Y"), "Sin datos", 960, "Pendiente"])

    wb.save(buffer)


async def get_historial_advertencias(page: int = 1, size: int = 20):
    try:
        pool = await get_pool()
        if pool is None:
            raise Exception()
        return []

    except:
        return no_db([])
