# apps/gestion/infrastructure/views.py
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from apps.gestion.application.services import DashboardService, HorarioService, RecuperacionService
from apps.gestion.infrastructure.serializers import (
    practicante_to_dict,
    horario_to_dict,
    recuperacion_to_dict, # Se asume que recuperacion_to_dict es el serializer correcto para la respuesta final.
    # Si la función get_detalle_recuperacion usa rechazo_recuperacion_to_dict,
    # deberías importarla aquí:
    # rechazo_recuperacion_to_dict
)
from apps.gestion.infrastructure.django_orm_repository import PracticanteRepository

# -----------------------------
#      REPOSITORIOS Y SERVICIOS
# -----------------------------
practicante_repo = PracticanteRepository()
dashboard_service = DashboardService(practicante_repo)
horario_service = HorarioService(practicante_repo)
recuperacion_service = RecuperacionService(practicante_repo)

# -----------------------------
#      DASHBOARD SUMMARY
# -----------------------------
def get_dashboard_summary(request):
    # Ya era síncrono, se mantiene.
    result = dashboard_service.get_summary()
    return JsonResponse(result, safe=False)

# -----------------------------
#      VISTA SEMANAL
# -----------------------------
def get_vista_semanal(request):
    # Ya era síncrono, se mantiene.
    result = horario_service.get_vista_semanal()
    return JsonResponse(result, safe=False)

# -----------------------------
#      PRACTICANTES
# -----------------------------
# CORREGIDO: Se añadió 'async' y 'await' para resolver el TypeError.
async def listar_practicantes(request):
    practicantes = await practicante_repo.list_all_with_horario() # AHORA ES ASÍNCRONO
    data = [practicante_to_dict(p) for p in practicantes]
    return JsonResponse(data, safe=False)

# CORREGIDO: Se asume que get_with_horario() es asíncrono y se añade 'async' y 'await'.
async def get_horario_practicante(request, practicante_id):
    practicante = await practicante_repo.get_with_horario(practicante_id)
    if not practicante:
        raise Http404("Practicante no encontrado")
    return JsonResponse(horario_to_dict(practicante.horarios), safe=False)

@csrf_exempt
def actualizar_horario_practicante(request, practicante_id):
    if request.method != "POST" and request.method != "PUT":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    data = request.POST.dict()
    # Se asume que esta función es síncrona o usa asgiref.sync_to_async internamente
    horario_service.actualizar_horario(practicante_id, data)
    return JsonResponse({"message": "Horario actualizado"})

# -----------------------------
#      RECUPERACIONES
# -----------------------------
def get_pendientes_aprobacion(request):
    result = recuperacion_service.get_pendientes()
    return JsonResponse(result, safe=False)

def get_detalle_recuperacion(request, id):
    rec = recuperacion_service.get_by_id(id)
    if not rec:
        raise Http404("No encontrado")
        
    # ATENCIÓN: Esta línea probablemente causará un NameError si 'rechazo_recuperacion_to_dict' no está importada.
    # Se reemplaza por la importación asumida 'recuperacion_to_dict', si es el serializer correcto, o 
    # se debe añadir 'rechazo_recuperacion_to_dict' a la lista de imports.
    # Por ahora, se asume que existe y se mantiene el nombre original del código proporcionado, 
    # pero asegúrate de que esté en tu archivo serializers.py y esté importado.
    return JsonResponse(recuperacion_to_dict(rec), safe=False) # Usando recuperacion_to_dict o asegúrate de importar el correcto.

@csrf_exempt
def aprobar_recuperacion(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    recuperacion_service.aprobar(id)
    return JsonResponse({"message": "Recuperación aprobada"})

@csrf_exempt
def rechazar_recuperacion(request, id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)
    motivo = request.POST.get("motivo", "")
    recuperacion_service.rechazar(id, motivo)
    return JsonResponse({"message": "Recuperación rechazada"})

# -----------------------------
#      REGISTRO CON EVIDENCIA
# -----------------------------
@csrf_exempt
def registrar_horario_con_evidencia(request, practicante_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    foto = request.FILES.get("foto")
    bloques = request.POST.get("bloques", "[]")

    horario_service.registrar_con_evidencia(practicante_id, foto.read(), bloques)
    return JsonResponse({"message": "Horario enviado para aprobación"})

# -----------------------------
#      SERVIDORES
# -----------------------------
def get_servidores(request):
    data = ["Rpsoft", "SENATI", "Innovación", "MiniBootcamp", "Laboratorios", "Recuperación"]
    return JsonResponse(data, safe=False)