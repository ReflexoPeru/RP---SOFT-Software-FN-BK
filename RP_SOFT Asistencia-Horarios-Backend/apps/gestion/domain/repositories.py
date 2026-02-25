from abc import ABC, abstractmethod
from typing import List, Dict, Any

class PracticanteRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Any]:
        pass
    
    @abstractmethod
    async def get_by_id(self, id: int) -> Any:
        pass
    
    @abstractmethod
    async def get_with_horario(self, id: int) -> Any:
        pass
    
    @abstractmethod
    async def list_all_with_horario(self) -> List[Any]:
        pass

class AsistenciaRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Any]:
        pass

class HorarioRepository(ABC):
    @abstractmethod
    async def create(self, data: Dict) -> Any:
        pass

class AdvertenciaRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Any]:
        pass
