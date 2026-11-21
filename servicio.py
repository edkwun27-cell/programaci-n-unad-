"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: servicio.py
Descripción: Clase abstracta Servicio y tres servicios especializados.
Demuestra herencia, polimorfismo y métodos sobrecargados (vía parámetros opcionales).
"""

from abc import abstractmethod
from typing import Any, Dict
from entidad import Entidad
from exceptions import ServicioInvalidoError, ParametrosInvalidosError


class Servicio(Entidad):
    """
    Clase abstracta que representa un servicio ofrecido por Software FJ.
    """

    def __init__(self, id_servicio: str, nombre: str, costo_base: float):
        super().__init__(id_servicio)
        if not nombre or len(nombre.strip()) < 3:
            raise ServicioInvalidoError("El nombre del servicio debe tener al menos 3 caracteres.")
        if costo_base < 0:
            raise ServicioInvalidoError("El costo base no puede ser negativo.")
        self._nombre = nombre.strip()
        self._costo_base = float(costo_base)
        self._disponible = True

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def costo_base(self) -> float:
        return self._costo_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    def marcar_no_disponible(self) -> None:
        self._disponible = False

    # Métodos abstractos (polimorfismo)
    @abstractmethod
    def calcular_costo(self, duracion: float, **kwargs) -> float:
        """Calcula el costo total. Debe ser implementado por las subclases."""
        pass

    @abstractmethod
    def describir(self) -> str:
        """Descripción detallada del servicio."""
        pass

    @abstractmethod
    def validar_parametros(self, **kwargs) -> None:
        """Valida parámetros específicos del servicio."""
        pass

    # Método sobrecargado simulado (parámetros opcionales)
    def calcular_costo_con_impuestos(self, duracion: float, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Variante sobrecargada: calcula costo aplicando impuesto y descuento.
        Demuestra métodos con parámetros opcionales.
        """
        costo = self.calcular_costo(duracion)
        if descuento < 0 or descuento > 1:
            raise ParametrosInvalidosError("El descuento debe estar entre 0 y 1.")
        if impuesto < 0:
            raise ParametrosInvalidosError("El impuesto no puede ser negativo.")
        costo_con_desc = costo * (1 - descuento)
        return round(costo_con_desc * (1 + impuesto), 2)

    def obtener_info(self) -> str:
        estado = "Disponible" if self.disponible else "No disponible"
        return f"Servicio[{self.id}] - {self.nombre} | Base: ${self.costo_base:.2f} | {estado}"

    def validar(self) -> bool:
        return self.disponible and self.costo_base >= 0


# === Servicios especializados ===

class ReservaSala(Servicio):
    """Servicio de reserva de salas de reuniones."""

    def __init__(self, id_servicio: str, nombre: str, costo_base: float, capacidad: int, ubicacion: str):
        super().__init__(id_servicio, nombre, costo_base)
        if capacidad <= 0:
            raise ServicioInvalidoError("La capacidad de la sala debe ser positiva.")
        self._capacidad = capacidad
        self._ubicacion = ubicacion

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        if duracion <= 0:
            raise ParametrosInvalidosError("La duración debe ser mayor a 0.")
        # Costo por hora
        return round(self.costo_base * duracion, 2)

    def describir(self) -> str:
        return f"Reserva de sala '{self.nombre}' (Capacidad: {self._capacidad}, Ubicación: {self._ubicacion})"

    def validar_parametros(self, **kwargs) -> None:
        personas = kwargs.get("personas")
        if personas is not None and (not isinstance(personas, int) or personas > self._capacidad or personas <= 0):
            raise ParametrosInvalidosError(f"Número de personas inválido. Máximo: {self._capacidad}")


class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnológicos."""

    def __init__(self, id_servicio: str, nombre: str, costo_base: float, tipo_equipo: str, cantidad_disponible: int):
        super().__init__(id_servicio, nombre, costo_base)
        if cantidad_disponible <= 0:
            raise ServicioInvalidoError("La cantidad disponible debe ser positiva.")
        self._tipo_equipo = tipo_equipo
        self._cantidad_disponible = cantidad_disponible

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        if duracion <= 0:
            raise ParametrosInvalidosError("La duración debe ser mayor a 0.")
        cantidad = kwargs.get("cantidad", 1)
        if cantidad > self._cantidad_disponible:
            raise ServicioInvalidoError(f"Cantidad solicitada ({cantidad}) supera lo disponible ({self._cantidad_disponible})")
        return round(self.costo_base * duracion * cantidad, 2)

    def describir(self) -> str:
        return f"Alquiler de {self._tipo_equipo} - {self.nombre} (Disponibles: {self._cantidad_disponible})"

    def validar_parametros(self, **kwargs) -> None:
        cantidad = kwargs.get("cantidad", 1)
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ParametrosInvalidosError("La cantidad debe ser un entero positivo.")


class AsesoriaEspecializada(Servicio):
    """Servicio de asesorías especializadas."""

    def __init__(self, id_servicio: str, nombre: str, costo_base: float, nivel: str, especialista: str):
        super().__init__(id_servicio, nombre, costo_base)
        niveles_validos = ["básico", "intermedio", "avanzado"]
        if nivel.lower() not in niveles_validos:
            raise ServicioInvalidoError(f"Nivel inválido. Use: {niveles_validos}")
        self._nivel = nivel.lower()
        self._especialista = especialista

    def calcular_costo(self, duracion: float, **kwargs) -> float:
        if duracion <= 0:
            raise ParametrosInvalidosError("La duración debe ser mayor a 0.")
        multiplicador = {"básico": 1.0, "intermedio": 1.3, "avanzado": 1.6}.get(self._nivel, 1.0)
        return round(self.costo_base * duracion * multiplicador, 2)

    def describir(self) -> str:
        return f"Asesoría {self._nivel.capitalize()} con {self._especialista} - {self.nombre}"

    def validar_parametros(self, **kwargs) -> None:
        # Validación específica opcional
        tema = kwargs.get("tema")
        if tema is not None and len(str(tema).strip()) < 3:
            raise ParametrosInvalidosError("El tema de la asesoría es muy corto.")
