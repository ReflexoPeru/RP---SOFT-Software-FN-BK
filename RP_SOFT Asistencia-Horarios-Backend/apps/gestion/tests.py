# tests.py

from django.test import TestCase
from unittest.mock import patch, MagicMock
from django.urls import reverse
from apps.gestion.infrastructure.views import listar_practicantes

# --- Datos Falsos para el Mock ---
# El Mock debe devolver objetos que se parezcan a los que devuelve tu ORM.
class MockPracticante:
    def __init__(self, id, nombre, horario):
        self.id = id
        self.nombre = nombre
        self.horarios = horario # Asegúrate de que tenga el atributo 'horarios'

MOCK_PRACTICANTES = [
    MockPracticante(id=1, nombre="Alice", horario=[{'dia': 'Lunes'}]),
    MockPracticante(id=2, nombre="Bob", horario=[{'dia': 'Martes'}]),
]

# ----------------------------------------------------------------------

class PracticanteViewTests(TestCase):

    # 1. PRUEBA PARA LISTAR PRACTICANTES (Ruta /practicantes/)
    # Usamos @patch para simular la respuesta del repositorio
    @patch('apps.gestion.infrastructure.django_orm_repository.PracticanteRepository.list_all_with_horario')
    async def test_listar_practicantes_ok(self, mock_list_all):
        
        # 1. Configurar el Mock: Le decimos al método del repositorio qué debe devolver.
        # Debe ser una coroutine que devuelve la lista, por eso usamos MagicMock().
        mock_list_all.return_value = MOCK_PRACTICANTES 
        
        # 2. Hacer la solicitud (usando reverse con el nombre de la URL)
        response = await self.async_client.get(reverse('listar_practicantes'))
        
        # 3. Afirmaciones
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json()[0]['nombre'], 'Alice')
        
        # Opcional: Asegurarse de que el repositorio fue llamado
        mock_list_all.assert_called_once()
        
    # 2. PRUEBA PARA OBTENER HORARIO (Ruta /practicantes/<id>/horario/)
    @patch('apps.gestion.infrastructure.django_orm_repository.PracticanteRepository.get_with_horario')
    async def test_get_horario_practicante_ok(self, mock_get_horario):
        
        # Configurar el Mock: El repositorio devuelve un solo objeto.
        mock_get_horario.return_value = MOCK_PRACTICANTES[0]

        # Hacer la solicitud
        response = await self.async_client.get(reverse('horario_practicante', kwargs={'practicante_id': 1}))
        
        # Afirmaciones
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Lunes' in response.json()[0].values())
        
    # 3. PRUEBA DE DATOS NO ENCONTRADOS (Simulando el 404 que ya veías)
    @patch('apps.gestion.infrastructure.django_orm_repository.PracticanteRepository.get_with_horario')
    async def test_get_horario_practicante_not_found(self, mock_get_horario):
        
        # Configurar el Mock: El repositorio devuelve None (simulando que no encontró datos)
        mock_get_horario.return_value = None 

        # Hacer la solicitud
        response = await self.async_client.get(reverse('horario_practicante', kwargs={'practicante_id': 99}))
        
        # Afirmación: Esperamos que el código 404 sea devuelto.
        self.assertEqual(response.status_code, 404)