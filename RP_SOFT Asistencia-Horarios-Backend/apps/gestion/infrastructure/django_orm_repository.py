from typing import List, Any
from apps.gestion.domain.repositories import PracticanteRepository

class PracticanteRepository(PracticanteRepository):
    def __init__(self):
        self.practicantes = []
    
    async def get_all(self) -> List[Any]:
        return self.practicantes
    
    async def get_by_id(self, id: int) -> Any:
        for p in self.practicantes:
            if p.id == id:
                return p
        return None
    
    async def get_with_horario(self, id: int) -> Any:
        return await self.get_by_id(id)
    
    async def list_all_with_horario(self) -> List[Any]:
        return self.practicantes
