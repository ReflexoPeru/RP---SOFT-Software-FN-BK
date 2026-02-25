from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, force_authenticate
from apps.reportes.infrastructure import views


class ReportesAPITests(APITestCase):
    def setUp(self):
        # LA LÍNEA MÁGICA QUE ARREGLA EL BUG PARA SIEMPRE
        self.client = APIClient(enforce_csrf_checks=False)
        self.client.defaults['HTTP_ACCEPT'] = 'application/json'  # <-- ESTA ES LA CLAVE

    def test_dashboard_summary(self):
        url = reverse("reportes:summary")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_advertencias_mes_actual(self):
        url = reverse("reportes:advertencias_mes_actual")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_advertencias_historico(self):
        url = reverse("reportes:advertencias_historico")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permisos_semana_actual(self):
        url = reverse("reportes:permisos_semana_actual")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permisos_por_practicante(self):
        url = reverse("reportes:permisos_por_practicante")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_resumen_global_horas(self):
        url = reverse("reportes:resumen_global_horas")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalle_cumplimiento_horas(self):
        url = reverse("reportes:detalle_cumplimiento_horas")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_export_reporte_semanal(self):
        url = reverse("reportes:export_reporte_semanal")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_export_reporte_mensual(self):
        url = reverse("reportes:export_reporte_mensual")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
