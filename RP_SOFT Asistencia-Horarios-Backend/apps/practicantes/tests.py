import unittest
from apps.practicantes.domain.practicante import Practicante, EstadoPracticante
from apps.practicantes.infrastructure.in_memory_repository import InMemoryPracticanteRepository
from apps.practicantes.application.services import PracticanteService

# --- Tests para la Capa de Dominio ---
class PracticanteDomainTest(unittest.TestCase):

    def test_creacion_practicante_valido(self):
        practicante = Practicante(
            id_discord=123,
            nombre="Juan",
            apellido="Perez",
            correo="juan@test.com",
            semestre=5,
            estado=EstadoPracticante.ACTIVO
        )
        self.assertEqual(practicante.nombre_completo, "Juan Perez")
        self.assertEqual(practicante.estado, EstadoPracticante.ACTIVO)

    def test_creacion_practicante_semestre_invalido(self):
        with self.assertRaises(ValueError):
            Practicante(
                id_discord=123,
                nombre="Ana",
                apellido="Gomez",
                correo="ana@test.com",
                semestre=8  # Semestre inválido
            )

    def test_cambiar_estado(self):
        practicante = Practicante(id_discord=1, nombre="Test", apellido="User", correo="t@t.com", semestre=1)
        practicante.marcar_en_riesgo()
        self.assertEqual(practicante.estado, EstadoPracticante.EN_RIESGO)
        practicante.marcar_en_recuperacion()
        self.assertEqual(practicante.estado, EstadoPracticante.EN_RECUPERACION)
        practicante.activar()
        self.assertEqual(practicante.estado, EstadoPracticante.ACTIVO)

# --- Tests para la Capa de Aplicación ---
class PracticanteServiceTest(unittest.TestCase):

    def setUp(self):
        self.repository = InMemoryPracticanteRepository()
        self.service = PracticanteService(self.repository)
        
        # Datos iniciales
        self.practicante1_data = {'id_discord': 1, 'nombre': 'Juan', 'apellido': 'Perez', 'correo': 'juan.perez@test.com', 'semestre': 5, 'estado': EstadoPracticante.ACTIVO}
        self.practicante2_data = {'id_discord': 2, 'nombre': 'Maria', 'apellido': 'Gomez', 'correo': 'maria.gomez@test.com', 'semestre': 4, 'estado': EstadoPracticante.EN_RECUPERACION}
        self.practicante1 = self.service.create_practicante(self.practicante1_data)
        self.practicante2 = self.service.create_practicante(self.practicante2_data)

    def test_get_all_practicantes(self):
        practicantes = self.service.get_all_practicantes()
        self.assertEqual(len(practicantes), 2)

    def test_get_practicante_by_id(self):
        practicante = self.service.get_practicante_by_id(self.practicante1.id)
        self.assertEqual(practicante.nombre, 'Juan')

    def test_create_practicante(self):
        nuevo_practicante_data = {'id_discord': 3, 'nombre': 'Pedro', 'apellido': 'Lopez', 'correo': 'pedro.lopez@test.com', 'semestre': 3, 'estado': 'en_riesgo'}
        practicante = self.service.create_practicante(nuevo_practicante_data)
        self.assertIsNotNone(practicante.id)
        self.assertEqual(practicante.nombre, 'Pedro')
        self.assertEqual(len(self.service.get_all_practicantes()), 3)

    def test_update_practicante(self):
        update_data = {'nombre': 'Juanito', 'estado': 'en_riesgo'}
        practicante_actualizado = self.service.update_practicante(self.practicante1.id, update_data)
        self.assertEqual(practicante_actualizado.nombre, 'Juanito')
        self.assertEqual(practicante_actualizado.estado, EstadoPracticante.EN_RIESGO)

    def test_delete_practicante(self):
        self.service.delete_practicante(self.practicante1.id)
        practicante = self.service.get_practicante_by_id(self.practicante1.id)
        self.assertIsNone(practicante)
        self.assertEqual(len(self.service.get_all_practicantes()), 1)

    def test_filter_practicantes(self):
        practicantes = self.service.filter_practicantes(nombre='Juan')
        self.assertEqual(len(practicantes), 1)
        self.assertEqual(practicantes[0].nombre, 'Juan')

    def test_get_practicante_stats(self):
        stats = self.service.get_practicante_stats()
        self.assertEqual(stats['total'], 2)
        self.assertEqual(stats['activos'], 1)
        self.assertEqual(stats['en_recuperacion'], 1)
        self.assertEqual(stats['en_riesgo'], 0)
