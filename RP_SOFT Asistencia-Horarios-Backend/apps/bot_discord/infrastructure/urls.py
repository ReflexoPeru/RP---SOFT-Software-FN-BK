from django.urls import path
from .views import MetricasBotView, ResumenBotView, EstadoBotView, ServidoresBotView, BotStatusUpdateView

urlpatterns = [
    path('metrics/', MetricasBotView.as_view(), name='bot-metrics'),
    path('status/', BotStatusUpdateView.as_view(), name='bot-status-update'),
    path('resumen/', ResumenBotView.as_view(), name='bot-resumen'),
    path('estado/', EstadoBotView.as_view(), name='bot-estado'),
    path('servers/', ServidoresBotView.as_view(), name='bot-servers'),
]
