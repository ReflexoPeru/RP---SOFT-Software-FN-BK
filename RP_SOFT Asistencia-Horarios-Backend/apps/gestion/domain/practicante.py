from typing import List, Optional

class Practicante:
    def __init__(self, id: int, nombre: str, apellido: str, servidor: Optional[str] = None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.servidor = servidor
        self.horarios = []
        self.estado = "ACTIVO"
