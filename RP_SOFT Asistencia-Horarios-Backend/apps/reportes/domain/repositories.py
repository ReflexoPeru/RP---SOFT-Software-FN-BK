# app/domain/repositories.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import date

class IReporteRepository(ABC):

    @abstractmethod
    async def get_total_horas_trabajadas_periodo_actual(self) -> float:
        pass

    @abstractmethod
    async def get_advertencias_mes_actual(self) -> List[Dict]:
        pass

    @abstractmethod
    async def get_historial_advertencias(self, page: int, size: int) -> List[Dict]:
        pass

    @abstractmethod
    async def get_cumplimiento_semanal_detalle(self) -> List[Dict]:
        pass

    @abstractmethod
    async def get_resumen_global_horas(self) -> Dict:
        pass

    @abstractmethod
    async def get_permisos_semana_actual(self) -> List[Dict]:
        pass

    @abstractmethod
    async def get_resumen_permisos_por_practicante(self) -> List[Dict]:
        pass

    @abstractmethod
    async def generar_datos_reporte_semanal(self) -> List[Dict]:
        pass

    @abstractmethod
    async def generar_datos_reporte_mensual(self) -> List[Dict]:
        pass