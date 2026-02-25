from typing import Dict, List, Optional
from django.db.models import Q
from apps.practicantes.domain.practicante import Practicante, EstadoPracticante
from apps.practicantes.domain.repositories import PracticanteRepository

# Implementación de un repositorio en memoria para los tests
class InMemoryPracticanteRepository(PracticanteRepository):
    
    def __init__(self):
        self._practicantes: Dict[int, Practicante] = {}
        self._next_id = 1

    def get_all(self) -> List[Practicante]:
        return list(self._practicantes.values())

    def get_by_id(self, practicante_id: int) -> Optional[Practicante]:
        return self._practicantes.get(practicante_id)

    def create(self, practicante: Practicante) -> Practicante:
        practicante.id = self._next_id
        self._practicantes[self._next_id] = practicante
        self._next_id += 1
        return practicante

    def update(self, practicante: Practicante) -> Practicante:
        if practicante.id in self._practicantes:
            self._practicantes[practicante.id] = practicante
            return practicante
        return None

    def delete(self, practicante_id: int) -> None:
        if practicante_id in self._practicantes:
            del self._practicantes[practicante_id]

    def filter(self, nombre: Optional[str] = None, correo: Optional[str] = None, estado: Optional[str] = None) -> List[Practicante]:
        results = list(self._practicantes.values())
        if nombre:
            results = [p for p in results if nombre.lower() in p.nombre.lower()]
        if correo:
            results = [p for p in results if correo.lower() in p.correo.lower()]
        if estado:
            results = [p for p in results if p.estado.value == estado]
        return results

    def get_stats(self) -> dict:
        stats = {"total": 0, "activos": 0, "en_recuperacion": 0, "en_riesgo": 0}
        for p in self._practicantes.values():
            stats["total"] += 1
            if p.estado == EstadoPracticante.ACTIVO:
                stats["activos"] += 1
            elif p.estado == EstadoPracticante.EN_RECUPERACION:
                stats["en_recuperacion"] += 1
            elif p.estado == EstadoPracticante.EN_RIESGO:
                stats["en_riesgo"] += 1
        return stats
