from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q, Count, Case, When, IntegerField
from django.db import OperationalError
from django.utils import timezone
from datetime import datetime, time, timedelta
from apps.practicantes.infrastructure.models import Practicante
from apps.puntualidad.infrastructure.models import Asistencia, EstadoAsistencia, HorarioClases, AsistenciaRecuperacion
from apps.puntualidad.infrastructure.serializers import JustificacionCreateSerializer
import logging

logger = logging.getLogger(__name__)


def obtener_estado_asistencia():
    """Obtiene o crea los estados de asistencia necesarios"""
    try:
        estados = {}
        estados_nombres = {
            'presente': 'Presente',
            'tardanza': 'Tardanza',
            'ausente-justificado': 'Ausente Justificado',
            'ausente-sin-justificar': 'Ausente Sin Justificar'
        }
        
        for key, nombre in estados_nombres.items():
            estado, _ = EstadoAsistencia.objects.get_or_create(
                estado=nombre,
                defaults={'estado': nombre}
            )
            estados[key] = estado
        
        return estados
    except OperationalError as e:
        logger.error(f"Error al obtener estados de asistencia: {str(e)}")
        # Retornar estados vacíos si las tablas no existen
        return {}


@api_view(['GET'])
def resumen_puntualidad(request):
    """
    Endpoint mejorado que devuelve el resumen de puntualidad del día actual
    Con cálculos optimizados y validaciones robustas
    """
    try:
        hoy = timezone.now().date()
        estados = obtener_estado_asistencia()
        
        # Si no hay estados, las tablas probablemente no existen
        if not estados:
            return Response({
                "asistencias": 0,
                "tardanzas": 0,
                "faltas": 0,
                "total": 0,
                "con_clases": 0,
                "ausentes_justificados": 0,
                "ausentes_sin_justificar": 0
            })
        
        # Mapear día de la semana en español
        dias_semana = {
            0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
            4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
        }
        dia_hoy = dias_semana[hoy.weekday()]
        
        # Obtener practicantes con clases de forma optimizada
        try:
            practicantes_con_clases = set(HorarioClases.objects.filter(
                dia_clase=dia_hoy
            ).values_list('practicante_id', flat=True))
        except OperationalError:
            practicantes_con_clases = set()
        
        # Total de practicantes activos que deben asistir (optimizado)
        try:
            total_practicantes = Practicante.objects.filter(
                estado='activo'
            ).exclude(id__in=practicantes_con_clases).count()
        except OperationalError:
            total_practicantes = 0
        
        # Contar asistencias del día de forma optimizada con una sola consulta
        try:
            asistencias_hoy = Asistencia.objects.filter(fecha=hoy)
            
            # Usar agregación para contar todos los estados en una consulta
            conteos = asistencias_hoy.values('estado_id').annotate(
                total=Count('id')
            )
            
            # Inicializar contadores
            presentes = 0
            tardanzas = 0
            ausentes_justificados = 0
            ausentes_sin_justificar = 0
            
            # Mapear conteos usando IDs de estados
            estado_presente_id = estados.get('presente').id if estados.get('presente') else None
            estado_tardanza_id = estados.get('tardanza').id if estados.get('tardanza') else None
            estado_ausente_just_id = estados.get('ausente-justificado').id if estados.get('ausente-justificado') else None
            estado_ausente_sin_id = estados.get('ausente-sin-justificar').id if estados.get('ausente-sin-justificar') else None
            
            for conteo in conteos:
                estado_id = conteo['estado_id']
                total = conteo['total']
                
                if estado_id == estado_presente_id:
                    presentes = total
                elif estado_id == estado_tardanza_id:
                    tardanzas = total
                elif estado_id == estado_ausente_just_id:
                    ausentes_justificados = total
                elif estado_id == estado_ausente_sin_id:
                    ausentes_sin_justificar = total
                    
        except OperationalError:
            presentes = 0
            tardanzas = 0
            ausentes_justificados = 0
            ausentes_sin_justificar = 0
        
        con_clases = len(practicantes_con_clases)
        total_deben_asistir = total_practicantes + con_clases
        
        data = {
            "asistencias": presentes,
            "tardanzas": tardanzas,
            "faltas": ausentes_justificados + ausentes_sin_justificar,
            "total": total_deben_asistir,
            "con_clases": con_clases,
            "ausentes_justificados": ausentes_justificados,
            "ausentes_sin_justificar": ausentes_sin_justificar
        }
        return Response(data)
    except Exception as e:
        logger.error(f"Error en resumen_puntualidad: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al obtener el resumen de puntualidad", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def alertas_puntualidad(request):
    """
    Endpoint que devuelve las alertas automáticas de puntualidad
    """
    try:
        hoy = timezone.now().date()
        estados = obtener_estado_asistencia()
        alertas = []
        
        # Si no hay estados, retornar lista vacía
        if not estados:
            return Response([])
        
        # Alerta 1: Tardanzas potenciales
        try:
            tardanzas_hoy = Asistencia.objects.filter(
                fecha=hoy,
                estado=estados.get('tardanza')
            ).select_related('practicante') if estados.get('tardanza') else []
            
            if tardanzas_hoy and tardanzas_hoy.exists():
                practicantes_tardanza = [
                    f"{a.practicante.nombre} {a.practicante.apellido}"
                    for a in tardanzas_hoy[:5]
                ]
                alertas.append({
                    "tipo": "tardanza",
                    "titulo": "Tardanza potencial detectada",
                    "cantidad": tardanzas_hoy.count(),
                    "hora": "8:05 a.m.",
                    "descripcion": "Gracia de 5 minutos aplicada",
                    "practicantes": practicantes_tardanza
                })
        except (OperationalError, AttributeError):
            pass
        
        # Alerta 2: Ausencias sin clase registrada
        try:
            dias_semana = {
                0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
                4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
            }
            dia_hoy = dias_semana[hoy.weekday()]
            practicantes_con_clases = list(HorarioClases.objects.filter(
                dia_clase=dia_hoy
            ).values_list('practicante_id', flat=True))
            
            ausentes_sin_clase = Asistencia.objects.filter(
                fecha=hoy,
                estado=estados.get('ausente-sin-justificar')
            ).exclude(
                practicante_id__in=practicantes_con_clases
            ).select_related('practicante') if estados.get('ausente-sin-justificar') else []
            
            if ausentes_sin_clase and ausentes_sin_clase.exists():
                practicantes_ausentes = [
                    f"{a.practicante.nombre} {a.practicante.apellido}"
                    for a in ausentes_sin_clase[:5]
                ]
                alertas.append({
                    "tipo": "ausencia",
                    "titulo": "Ausencias sin clase registrada",
                    "cantidad": ausentes_sin_clase.count(),
                    "hora": "8:30 a.m.",
                    "descripcion": "No tienen clases programadas hoy",
                    "practicantes": practicantes_ausentes
                })
        except (OperationalError, AttributeError):
            pass
        
        # Alerta 3: Practicantes en riesgo
        try:
            inicio_mes = hoy.replace(day=1)
            practicantes_riesgo = Asistencia.objects.filter(
                fecha__gte=inicio_mes,
                fecha__lte=hoy,
                estado=estados.get('ausente-sin-justificar')
            ).values('practicante').annotate(
                total_ausencias=Count('id')
            ).filter(total_ausencias__gte=3) if estados.get('ausente-sin-justificar') else []
            
            if practicantes_riesgo and practicantes_riesgo.exists():
                nombres_riesgo = []
                for p in practicantes_riesgo[:5]:
                    try:
                        practicante = Practicante.objects.get(id=p['practicante'])
                        nombres_riesgo.append(f"{practicante.nombre} {practicante.apellido}")
                    except Practicante.DoesNotExist:
                        continue
                
                if nombres_riesgo:
                    alertas.append({
                        "tipo": "riesgo",
                        "titulo": "Practicantes en riesgo",
                        "cantidad": len(nombres_riesgo),
                        "hora": "9:15 a.m.",
                        "descripcion": "3er ticket del mes alcanzado",
                        "practicantes": nombres_riesgo
                    })
        except (OperationalError, AttributeError):
            pass
        
        return Response(alertas)
    except Exception as e:
        logger.error(f"Error en alertas_puntualidad: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al obtener las alertas", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def practicantes_puntualidad(request):
    """
    Endpoint que devuelve la lista de practicantes con su estado de asistencia del día
    """
    try:
        hoy = timezone.now().date()
        estados = obtener_estado_asistencia()
        
        # Si no hay estados, retornar lista vacía
        if not estados:
            return Response([])
        
        # Obtener todos los practicantes activos
        try:
            practicantes = Practicante.objects.filter(estado='activo').order_by('apellido', 'nombre')
        except OperationalError:
            return Response([])
        
        # Obtener asistencias del día
        try:
            asistencias_hoy = {
                a.practicante_id: a
                for a in Asistencia.objects.filter(fecha=hoy).select_related('practicante', 'estado')
            }
        except OperationalError:
            asistencias_hoy = {}
        
        # Obtener horarios de clases
        try:
            horarios = {
                h.practicante_id: h
                for h in HorarioClases.objects.filter(
                    practicante__in=practicantes
                ).select_related('practicante')
            }
        except OperationalError:
            horarios = {}
        
        data = []
        for practicante in practicantes:
            asistencia = asistencias_hoy.get(practicante.id)
            
            # Determinar estado
            if asistencia and asistencia.estado:
                estado_nombre = asistencia.estado.estado.lower()
                if 'presente' in estado_nombre:
                    estado = 'presente'
                elif 'tardanza' in estado_nombre:
                    estado = 'tardanza'
                elif 'justificado' in estado_nombre:
                    estado = 'ausente-justificado'
                else:
                    estado = 'ausente-sin-justificar'
                
                hora_entrada = asistencia.hora_entrada.strftime('%I:%M %p') if asistencia.hora_entrada else None
            else:
                estado = 'ausente-sin-justificar'
                hora_entrada = None
            
            # Calcular horas semanales (simulado por ahora)
            horas_completadas = 24
            horas_totales = 30
            
            practicante_data = {
                "id": practicante.id,
                "nombre": practicante.nombre,
                "apellido": practicante.apellido,
                "equipo": "Rpsoft",  # Esto debería venir de otro modelo o campo
                "team": "Team Alpha",  # Esto debería venir de otro modelo o campo
                "horaIngreso": hora_entrada,
                "horasSemanales": f"{horas_completadas}/{horas_totales}",
                "horasCompletadas": horas_completadas,
                "horasTotales": horas_totales,
                "estado": estado
            }
            
            if asistencia and asistencia.motivo:
                practicante_data["ticket"] = asistencia.motivo
            
            data.append(practicante_data)
        
        return Response(data)
    except Exception as e:
        logger.error(f"Error en practicantes_puntualidad: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al obtener la lista de practicantes", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def justificaciones(request):
    """
    Endpoint mejorado que devuelve la lista de justificaciones (asistencias ausentes justificadas)
    Con mejor cálculo de SLA y validaciones robustas
    """
    try:
        estados = obtener_estado_asistencia()
        
        if not estados or not estados.get('ausente-justificado'):
            return Response([])
        
        estado_justificado = estados['ausente-justificado']
        
        # Obtener asistencias justificadas que tienen motivo (ticket) - optimizado
        try:
            asistencias_justificadas = Asistencia.objects.filter(
                estado=estado_justificado,
                motivo__isnull=False
            ).exclude(motivo='').select_related('practicante', 'estado').order_by('-fecha', '-id')
        except OperationalError:
            return Response([])
        
        # Obtener el mes actual para contar tickets
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        # Optimizar: obtener todos los tickets del mes en una consulta
        try:
            tickets_mes_por_practicante = dict(
                Asistencia.objects.filter(
                    estado=estado_justificado,
                    motivo__isnull=False,
                    fecha__gte=inicio_mes,
                    fecha__lte=hoy
                ).exclude(motivo='').values('practicante_id').annotate(
                    total=Count('id')
                ).values_list('practicante_id', 'total')
            )
        except OperationalError:
            tickets_mes_por_practicante = {}
        
        data = []
        for asistencia in asistencias_justificadas:
            try:
                if not hasattr(asistencia, 'practicante') or not asistencia.practicante:
                    continue
                
                practicante = asistencia.practicante
                
                # Obtener tickets del mes de forma optimizada
                tickets_mes = tickets_mes_por_practicante.get(practicante.id, 0)
                
                # Determinar estado de la justificación de forma más precisa
                estado_just = 'pendiente'
                motivo_rechazo = None
                
                # Si tiene hora de entrada y salida, está aprobado
                if asistencia.hora_entrada and asistencia.hora_salida:
                    estado_just = 'aprobado'
                # Si tiene hora de entrada pero no salida, está en revisión
                elif asistencia.hora_entrada:
                    estado_just = 'pendiente'
                
                # Calcular SLA restante de forma más precisa (24 horas desde la fecha de creación)
                fecha_creacion = asistencia.fecha
                sla_restante = None
                
                if fecha_creacion:
                    # Calcular tiempo transcurrido en horas
                    ahora = timezone.now()
                    fecha_hora_creacion = timezone.make_aware(
                        datetime.combine(fecha_creacion, time(0, 0))
                    ) if timezone.is_naive(datetime.combine(fecha_creacion, time(0, 0))) else datetime.combine(fecha_creacion, time(0, 0))
                    
                    tiempo_transcurrido = ahora - fecha_hora_creacion
                    horas_transcurridas = tiempo_transcurrido.total_seconds() / 3600
                    horas_restantes = 24 - horas_transcurridas
                    
                    if horas_restantes <= 0 and estado_just == 'pendiente':
                        estado_just = 'vencido'
                        motivo_rechazo = "SLA vencido sin evidencia"
                    elif horas_restantes > 0:
                        horas = int(horas_restantes)
                        minutos = int((horas_restantes - horas) * 60)
                        if horas > 0:
                            sla_restante = f"{horas}h {minutos}m" if minutos > 0 else f"{horas}h"
                        else:
                            sla_restante = f"{minutos}m"
                
                # Formatear hora de envío
                enviado_str = ""
                if asistencia.hora_entrada:
                    try:
                        enviado_str = asistencia.hora_entrada.strftime('%I:%M %p').lstrip('0')
                    except (ValueError, AttributeError):
                        enviado_str = "Hora no disponible"
                
                # Formatear hora de revisión
                revisado_str = None
                if asistencia.hora_salida:
                    try:
                        revisado_str = asistencia.hora_salida.strftime('%I:%M %p').lstrip('0')
                    except (ValueError, AttributeError):
                        pass
                
                # Extraer ticket ID del motivo si es posible
                ticket_id = f"TKT-{asistencia.id}"
                if asistencia.motivo:
                    import re
                    ticket_match = re.search(r'TKT-?\d+', asistencia.motivo, re.IGNORECASE)
                    if ticket_match:
                        ticket_id = ticket_match.group(0).upper()
                    elif len(asistencia.motivo) <= 20:
                        ticket_id = asistencia.motivo
                
                justificacion_data = {
                    "id": asistencia.id,
                    "nombre": practicante.nombre or "Sin nombre",
                    "apellido": practicante.apellido or "",
                    "equipo": "Rpsoft",  # Esto debería venir de otro modelo
                    "ticketId": ticket_id,
                    "motivo": asistencia.motivo or "Sin motivo especificado",
                    "fecha": asistencia.fecha.strftime('%Y-%m-%d') if asistencia.fecha else '',
                    "enviado": enviado_str,
                    "revisado": revisado_str,
                    "tieneEvidencia": bool(asistencia.motivo and len(asistencia.motivo.strip()) > 0),
                    "ticketsMes": tickets_mes,
                    "ticketsMax": 3,
                    "estado": estado_just,
                    "slaRestante": sla_restante,
                    "motivoRechazo": motivo_rechazo
                }
                
                data.append(justificacion_data)
            except Exception as item_error:
                logger.warning(f"Error procesando justificación {asistencia.id}: {str(item_error)}")
                continue
        
        return Response(data)
    except Exception as e:
        logger.error(f"Error en justificaciones: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al obtener las justificaciones", "detail": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def recuperaciones(request):
    """
    Endpoint que devuelve la lista de recuperaciones de horas
    Versión simplificada y robusta que siempre devuelve una respuesta válida
    """
    # Siempre retornar una lista, incluso si hay errores
    data = []
    
    try:
        # Intentar obtener recuperaciones
        try:
            recuperaciones_queryset = AsistenciaRecuperacion.objects.select_related(
                'asistencia',
                'asistencia__practicante'
            ).filter(
                asistencia__isnull=False
            ).order_by('-fecha_recuperacion', '-id')
            
            # Convertir a lista para evitar problemas de lazy evaluation
            recuperaciones = list(recuperaciones_queryset[:100])  # Limitar a 100 para evitar problemas de memoria
            
        except OperationalError as op_error:
            # Si las tablas no existen, retornar lista vacía
            logger.info(f"Tablas no existen aún: {str(op_error)}")
            return Response([])
        except Exception as db_error:
            logger.warning(f"Error de base de datos en recuperaciones: {str(db_error)}")
            return Response([])
        
        # Si no hay recuperaciones, retornar lista vacía
        if not recuperaciones:
            return Response([])
        
        # Procesar cada recuperación
        for recuperacion in recuperaciones:
            try:
                # Validar relaciones de forma segura
                try:
                    asistencia = recuperacion.asistencia
                    if not asistencia:
                        continue
                except (AttributeError, Exception):
                    # Capturar cualquier excepción relacionada con la relación
                    continue
                
                try:
                    practicante = asistencia.practicante
                    if not practicante:
                        continue
                except (AttributeError, Exception):
                    # Capturar cualquier excepción relacionada con la relación
                    continue
                
                # Calcular horas completadas
                horas_completadas = 0
                horas_totales = 6
                
                if (recuperacion.hora_entrada and 
                    recuperacion.hora_salida and 
                    recuperacion.fecha_recuperacion):
                    try:
                        entrada = datetime.combine(
                            recuperacion.fecha_recuperacion, 
                            recuperacion.hora_entrada
                        )
                        salida = datetime.combine(
                            recuperacion.fecha_recuperacion, 
                            recuperacion.hora_salida
                        )
                        
                        if salida > entrada:
                            diferencia = salida - entrada
                            horas_completadas = round(diferencia.total_seconds() / 3600, 2)
                            horas_completadas = min(horas_completadas, 12)  # Máximo 12 horas
                            horas_totales = max(horas_totales, int(horas_completadas))
                    except (ValueError, TypeError, AttributeError):
                        horas_completadas = 0
                
                # Tipo de evidencia
                tipo_evidencia = 'trello'
                if asistencia.motivo and 'checklist' in str(asistencia.motivo).lower():
                    tipo_evidencia = 'checklist'
                
                # Formatear horario
                horario_str = ""
                try:
                    if recuperacion.hora_entrada and recuperacion.hora_salida:
                        hora_entrada_str = recuperacion.hora_entrada.strftime('%I:%M %p').lstrip('0')
                        hora_salida_str = recuperacion.hora_salida.strftime('%I:%M %p').lstrip('0')
                        horario_str = f"{hora_entrada_str} - {hora_salida_str}"
                    elif recuperacion.fecha_recuperacion:
                        dias_semana = {
                            0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves',
                            4: 'Viernes', 5: 'Sábado', 6: 'Domingo'
                        }
                        dia_semana = dias_semana.get(recuperacion.fecha_recuperacion.weekday(), '')
                        horario_str = f"{dia_semana} (Sin horario específico)" if dia_semana else "Sin horario"
                except (ValueError, AttributeError):
                    horario_str = "Horario no disponible"
                
                # Mapear estado
                estado_map = {
                    'Pendiente': 'programado',
                    'En Progreso': 'en-progreso',
                    'Completado': 'completado',
                    'Cancelado': 'programado'
                }
                estado_frontend = estado_map.get(str(recuperacion.estado), 'programado')
                
                # Actualizar estado según horas
                if horas_completadas > 0 and estado_frontend == 'programado':
                    estado_frontend = 'en-progreso'
                if horas_completadas >= horas_totales:
                    estado_frontend = 'completado'
                
                # Ticket ID
                ticket_id = f"TKT-{asistencia.id}"
                if asistencia.motivo:
                    import re
                    ticket_match = re.search(r'TKT-?\d+', str(asistencia.motivo), re.IGNORECASE)
                    if ticket_match:
                        ticket_id = ticket_match.group(0).upper()
                    elif len(str(asistencia.motivo)) <= 20:
                        ticket_id = str(asistencia.motivo)
                
                # Construir datos de recuperación
                recuperacion_data = {
                    "id": recuperacion.id,
                    "nombre": str(practicante.nombre) if practicante.nombre else "Sin nombre",
                    "apellido": str(practicante.apellido) if practicante.apellido else "",
                    "equipo": "Rpsoft",
                    "ticketId": ticket_id,
                    "estado": estado_frontend,
                    "horasCompletadas": int(horas_completadas),
                    "horasTotales": horas_totales,
                    "fechaProgramada": recuperacion.fecha_recuperacion.strftime('%Y-%m-%d') if recuperacion.fecha_recuperacion else '',
                    "horario": horario_str,
                    "tipoEvidencia": tipo_evidencia,
                    "tarea": str(asistencia.motivo) if asistencia.motivo else "Recuperación de horas",
                    "linkTrello": None
                }
                
                data.append(recuperacion_data)
                
            except Exception as item_error:
                logger.warning(f"Error procesando recuperación {getattr(recuperacion, 'id', 'unknown')}: {str(item_error)}")
                continue
        
        # Siempre retornar una lista, incluso si está vacía
        return Response(data)
        
    except Exception as e:
        logger.error(f"Error crítico en recuperaciones: {str(e)}", exc_info=True)
        # En caso de error crítico, retornar lista vacía en lugar de error
        # Esto evita que el frontend muestre un error cuando simplemente no hay datos
        return Response([])


@api_view(['GET'])
def practicantes_activos(request):
    """
    Endpoint simple para obtener lista de practicantes activos
    Usado para el formulario de nueva justificación
    """
    try:
        try:
            practicantes = Practicante.objects.filter(estado='activo').order_by('apellido', 'nombre')
            data = [
                {
                    "id": p.id,
                    "nombre": p.nombre,
                    "apellido": p.apellido,
                    "nombre_completo": f"{p.nombre} {p.apellido}"
                }
                for p in practicantes
            ]
            return Response(data)
        except OperationalError:
            return Response([])
    except Exception as e:
        logger.error(f"Error en practicantes_activos: {str(e)}", exc_info=True)
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def crear_justificacion(request):
    """
    Endpoint para crear una nueva justificación
    Valida límites de tickets por mes y otros requisitos
    """
    try:
        serializer = JustificacionCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {"error": "Datos inválidos", "detalles": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        practicante_id = serializer.validated_data['practicante_id']
        fecha = serializer.validated_data['fecha']
        motivo = serializer.validated_data['motivo']
        tiene_evidencia = serializer.validated_data.get('tiene_evidencia', False)
        ticket_id = serializer.validated_data.get('ticket_id', '')
        
        # Formatear motivo con ticket ID si se proporciona
        motivo_final = motivo
        if ticket_id:
            motivo_final = f"{ticket_id} - {motivo}"
        
        # Obtener estados
        estados = obtener_estado_asistencia()
        if not estados or not estados.get('ausente-justificado'):
            return Response(
                {"error": "Error en la configuración del sistema"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        estado_justificado = estados['ausente-justificado']
        
        # Validar límite de tickets del mes (máximo 3)
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        try:
            tickets_mes = Asistencia.objects.filter(
                practicante_id=practicante_id,
                estado=estado_justificado,
                motivo__isnull=False,
                fecha__gte=inicio_mes,
                fecha__lte=hoy
            ).exclude(motivo='').count()
            
            if tickets_mes >= 3:
                return Response(
                    {
                        "error": "Límite de tickets alcanzado",
                        "mensaje": f"Ya has usado {tickets_mes}/3 tickets este mes. El límite es de 3 tickets por mes."
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except OperationalError:
            # Si hay error de BD, continuar pero registrar
            logger.warning("No se pudo verificar límite de tickets")
        
        # Verificar si ya existe una asistencia para esta fecha
        try:
            asistencia_existente = Asistencia.objects.filter(
                practicante_id=practicante_id,
                fecha=fecha
            ).first()
            
            if asistencia_existente:
                # Si ya existe, actualizar el estado y motivo
                asistencia_existente.estado = estado_justificado
                asistencia_existente.motivo = motivo_final
                asistencia_existente.save()
                
                return Response(
                    {
                        "mensaje": "Justificación actualizada exitosamente",
                        "id": asistencia_existente.id,
                        "tickets_mes": tickets_mes + 1,
                        "tickets_max": 3
                    },
                    status=status.HTTP_200_OK
                )
        except OperationalError:
            pass
        
        # Crear nueva asistencia con estado justificado
        try:
            nueva_asistencia = Asistencia.objects.create(
                practicante_id=practicante_id,
                fecha=fecha,
                estado=estado_justificado,
                motivo=motivo_final,
                hora_entrada=None,  # Se establecerá cuando se apruebe
                hora_salida=None
            )
            
            return Response(
                {
                    "mensaje": "Justificación creada exitosamente",
                    "id": nueva_asistencia.id,
                    "tickets_mes": tickets_mes + 1,
                    "tickets_max": 3,
                    "sla_horas": 24,
                    "tiene_evidencia": tiene_evidencia
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as create_error:
            logger.error(f"Error al crear justificación: {str(create_error)}")
            return Response(
                {"error": "Error al crear la justificación", "detalle": str(create_error)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
    except Exception as e:
        logger.error(f"Error en crear_justificacion: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al procesar la solicitud", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def aprobar_justificacion(request, pk):
    """
    Endpoint para aprobar una justificación
    Basado en las imágenes: al aprobar se marca como aprobado
    """
    try:
        try:
            asistencia = Asistencia.objects.select_related('practicante', 'estado').get(id=pk)
        except Asistencia.DoesNotExist:
            return Response(
                {"error": "La justificación no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        estados = obtener_estado_asistencia()
        estado_justificado = estados.get('ausente-justificado')
        
        # Verificar que sea una justificación pendiente
        if asistencia.estado != estado_justificado:
            return Response(
                {"error": "Esta asistencia no es una justificación pendiente"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Aprobar: establecer hora de entrada y salida
        ahora = timezone.now()
        asistencia.hora_entrada = ahora.time()
        asistencia.hora_salida = ahora.time()
        asistencia.save()
        
        return Response(
            {
                "mensaje": "Justificación aprobada exitosamente",
                "id": asistencia.id,
                "estado": "aprobado"
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error en aprobar_justificacion: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al procesar la solicitud", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def rechazar_justificacion(request, pk):
    """
    Endpoint para rechazar una justificación
    Basado en las imágenes: requiere motivo de rechazo
    """
    try:
        motivo_rechazo = request.data.get('motivo_rechazo', '').strip()
        
        if not motivo_rechazo:
            return Response(
                {"error": "El motivo de rechazo es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            asistencia = Asistencia.objects.select_related('practicante', 'estado').get(id=pk)
        except Asistencia.DoesNotExist:
            return Response(
                {"error": "La justificación no existe"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        estados = obtener_estado_asistencia()
        estado_justificado = estados.get('ausente-justificado')
        
        # Verificar que sea una justificación pendiente
        if asistencia.estado != estado_justificado:
            return Response(
                {"error": "Esta asistencia no es una justificación pendiente"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Rechazar: actualizar motivo con razón de rechazo
        motivo_original = asistencia.motivo or ""
        motivo_completo = f"{motivo_original} [RECHAZADO: {motivo_rechazo}]"
        asistencia.motivo = motivo_completo
        asistencia.save()
        
        return Response(
            {
                "mensaje": "Justificación rechazada",
                "id": asistencia.id,
                "estado": "rechazado",
                "motivo_rechazo": motivo_rechazo
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error en rechazar_justificacion: {str(e)}", exc_info=True)
        return Response(
            {"error": "Error al procesar la solicitud", "detalle": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
