"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: gestor.py
Descripción: Gestor central del sistema. Maneja listas de clientes, servicios y reservas.
Toda la gestión se hace en memoria (sin base de datos).
"""

from typing import List, Dict, Optional
from cliente import Cliente
from servicio import Servicio
from reserva import Reserva
from exceptions import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
    ParametrosInvalidosError,
    SoftwareFJError
)
from logger import logger


class GestorSistema:
    """
    Clase principal que gestiona el sistema integral.
    Usa listas y diccionarios internos.
    """

    def __init__(self):
        self.clientes: Dict[str, Cliente] = {}
        self.servicios: Dict[str, Servicio] = {}
        self.reservas: Dict[str, Reserva] = {}
        logger.info("Gestor del sistema inicializado.")

    def registrar_cliente(self, id_cliente: str, nombre: str, email: str, telefono: str) -> Cliente:
        """Registra un nuevo cliente con validaciones."""
        try:
            if id_cliente in self.clientes:
                raise ClienteInvalidoError(f"Ya existe un cliente con ID {id_cliente}.")
            cliente = Cliente(id_cliente, nombre, email, telefono)
            self.clientes[id_cliente] = cliente
            logger.info(f"Cliente registrado: {cliente}")
            return cliente
        except ClienteInvalidoError as e:
            logger.error(f"Error al registrar cliente: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al registrar cliente: {e}")
            raise ClienteInvalidoError("Error inesperado al crear cliente") from e

    def registrar_servicio(self, servicio: Servicio) -> Servicio:
        """Registra un servicio ya instanciado."""
        try:
            if servicio.id in self.servicios:
                raise ServicioInvalidoError(f"Ya existe un servicio con ID {servicio.id}.")
            if not servicio.validar():
                raise ServicioInvalidoError("El servicio no pasó la validación.")
            self.servicios[servicio.id] = servicio
            logger.info(f"Servicio registrado: {servicio}")
            return servicio
        except ServicioInvalidoError as e:
            logger.error(f"Error al registrar servicio: {e}")
            raise

    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, duracion: float) -> Reserva:
        """Crea una nueva reserva."""
        try:
            if id_reserva in self.reservas:
                raise ReservaInvalidaError(f"Ya existe una reserva con ID {id_reserva}.")
            cliente = self.clientes.get(id_cliente)
            if not cliente:
                raise ReservaInvalidaError(f"Cliente {id_cliente} no encontrado.")
            servicio = self.servicios.get(id_servicio)
            if not servicio:
                raise ReservaInvalidaError(f"Servicio {id_servicio} no encontrado.")
            
            reserva = Reserva(id_reserva, cliente, servicio, duracion)
            self.reservas[id_reserva] = reserva
            return reserva
        except (ReservaInvalidaError, ServicioInvalidoError, ParametrosInvalidosError) as e:
            logger.error(f"Error al crear reserva: {e}")
            raise
        except Exception as e:
            logger.error(f"Error inesperado al crear reserva: {e}")
            raise ReservaInvalidaError("Error inesperado al crear reserva") from e

    def obtener_cliente(self, id_cliente: str) -> Optional[Cliente]:
        return self.clientes.get(id_cliente)

    def obtener_servicio(self, id_servicio: str) -> Optional[Servicio]:
        return self.servicios.get(id_servicio)

    def obtener_reserva(self, id_reserva: str) -> Optional[Reserva]:
        return self.reservas.get(id_reserva)

    def listar_clientes(self) -> List[Cliente]:
        return list(self.clientes.values())

    def listar_servicios(self) -> List[Servicio]:
        return list(self.servicios.values())

    def listar_reservas(self) -> List[Reserva]:
        return list(self.reservas.values())

    def resumen(self) -> str:
        return (f"Resumen del sistema:\n"
                f"  - Clientes: {len(self.clientes)}\n"
                f"  - Servicios: {len(self.servicios)}\n"
                f"  - Reservas: {len(self.reservas)}")
