"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: entidad.py
Descripción: Clase abstracta base para las entidades del sistema.
"""

from abc import ABC, abstractmethod
from typing import Any


class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general del sistema.
    Define la estructura mínima (ID) y fuerza la implementación de métodos comunes.
    """

    def __init__(self, id_entidad: str):
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ValueError("El ID de la entidad no puede estar vacío.")
        self._id = id_entidad.strip()

    @property
    def id(self) -> str:
        return self._id

    @abstractmethod
    def obtener_info(self) -> str:
        """Retorna una representación legible de la entidad."""
        pass

    @abstractmethod
    def validar(self) -> bool:
        """Valida el estado interno de la entidad."""
        pass

    def __str__(self) -> str:
        return self.obtener_info()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"
