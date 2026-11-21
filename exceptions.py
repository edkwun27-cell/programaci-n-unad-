"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - Universidad Nacional Abierta y a Distancia (UNAD)
Archivo: exceptions.py
Descripción: Excepciones personalizadas del sistema.
"""

class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""
    def __init__(self, message: str = "Error en el sistema Software FJ"):
        self.message = message
        super().__init__(self.message)


class ClienteInvalidoError(SoftwareFJError):
    """Error por datos inválidos de un cliente."""
    def __init__(self, message: str = "Datos de cliente inválidos"):
        super().__init__(message)


class ServicioInvalidoError(SoftwareFJError):
    """Error por servicio inválido o no disponible."""
    def __init__(self, message: str = "Servicio inválido o no disponible"):
        super().__init__(message)


class ReservaInvalidaError(SoftwareFJError):
    """Error en la creación o procesamiento de una reserva."""
    def __init__(self, message: str = "Reserva inválida"):
        super().__init__(message)


class ParametrosInvalidosError(SoftwareFJError):
    """Error por parámetros faltantes o incorrectos."""
    def __init__(self, message: str = "Parámetros inválidos"):
        super().__init__(message)


class OperacionNoPermitidaError(SoftwareFJError):
    """Error por operación no permitida en el estado actual."""
    def __init__(self, message: str = "Operación no permitida"):
        super().__init__(message)
