"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: reserva.py
Descripción: Clase Reserva que integra cliente, servicio, duración y estado.
Implementa confirmación, cancelación y procesamiento con manejo de excepciones.
"""

from datetime import datetime
from typing import Optional
from cliente import Cliente
from servicio import Servicio
from exceptions import (
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametrosInvalidosError,
    ServicioInvalidoError
)
from logger import logger


class Reserva:
    """
    Representa una reserva de un servicio por un cliente.
    """

    ESTADOS_VALIDOS = ["pendiente", "confirmada", "cancelada", "procesada"]

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: float, fecha: Optional[str] = None):
        if not id_reserva or not id_reserva.strip():
            raise ReservaInvalidaError("ID de reserva inválido.")
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("El cliente debe ser una instancia de Cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("El servicio debe ser una instancia de Servicio.")
        if duracion <= 0:
            raise ParametrosInvalidosError("La duración debe ser mayor a 0.")

        self.id = id_reserva.strip()
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M")
        self.estado = "pendiente"
        self.costo_final: Optional[float] = None

        # Validar disponibilidad inicial
        if not servicio.disponible:
            raise ServicioInvalidoError(f"El servicio {servicio.nombre} no está disponible.")

        cliente.agregar_reserva(self.id)
        logger.info(f"Reserva {self.id} creada para cliente {cliente.id} - servicio {servicio.id}")

    def confirmar(self) -> None:
        """Confirma la reserva si está pendiente."""
        if self.estado != "pendiente":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado '{self.estado}'.")
        self.estado = "confirmada"
        logger.info(f"Reserva {self.id} confirmada.")

    def cancelar(self, motivo: str = "Sin motivo") -> None:
        """Cancela la reserva."""
        if self.estado in ["cancelada", "procesada"]:
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva en estado '{self.estado}'.")
        self.estado = "cancelada"
        logger.info(f"Reserva {self.id} cancelada. Motivo: {motivo}")

    def procesar(self, aplicar_impuesto: bool = True, descuento: float = 0.0) -> float:
        """
        Procesa la reserva: calcula costo final y cambia estado.
        Demuestra uso de métodos sobrecargados del servicio.
        """
        if self.estado not in ["pendiente", "confirmada"]:
            raise OperacionNoPermitidaError(f"No se puede procesar una reserva en estado '{self.estado}'.")

        try:
            # Validar parámetros del servicio
            self.servicio.validar_parametros()
            
            # Cálculo polimórfico
            if aplicar_impuesto:
                self.costo_final = self.servicio.calcular_costo_con_impuestos(self.duracion, descuento=descuento)
            else:
                self.costo_final = self.servicio.calcular_costo(self.duracion)
            
            self.estado = "procesada"
            logger.info(f"Reserva {self.id} procesada. Costo final: ${self.costo_final:.2f}")
            return self.costo_final
        except Exception as e:
            # Encadenamiento de excepciones
            logger.error(f"Error al procesar reserva {self.id}: {e}")
            raise ReservaInvalidaError(f"Fallo al procesar reserva {self.id}") from e

    def obtener_info(self) -> str:
        costo = f"${self.costo_final:.2f}" if self.costo_final is not None else "No calculado"
        return (f"Reserva[{self.id}] | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Duración: {self.duracion}h | "
                f"Estado: {self.estado} | Costo: {costo}")

    def __str__(self) -> str:
        return self.obtener_info()
