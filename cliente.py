"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: cliente.py
Descripción: Clase Cliente con encapsulación estricta y validaciones robustas.
"""

import re
from entidad import Entidad
from exceptions import ClienteInvalidoError


class Cliente(Entidad):
    """
    Representa un cliente de Software FJ.
    Datos personales encapsulados con validaciones estrictas.
    """

    def __init__(self, id_cliente: str, nombre: str, email: str, telefono: str):
        super().__init__(id_cliente)
        self._validar_datos(nombre, email, telefono)
        self._nombre = nombre.strip()
        self._email = email.strip().lower()
        self._telefono = telefono.strip()
        self._reservas: list[str] = []  # IDs de reservas asociadas

    def _validar_datos(self, nombre: str, email: str, telefono: str) -> None:
        """Valida los datos del cliente y lanza excepciones específicas."""
        if not nombre or len(nombre.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")

        # Validación básica de email
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, email.strip()):
            raise ClienteInvalidoError(f"Email inválido: {email}")

        # Teléfono: solo dígitos, mínimo 7
        if not telefono or not telefono.strip().isdigit() or len(telefono.strip()) < 7:
            raise ClienteInvalidoError("El teléfono debe contener solo dígitos y tener al menos 7 caracteres.")

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def email(self) -> str:
        return self._email

    @property
    def telefono(self) -> str:
        return self._telefono

    def agregar_reserva(self, id_reserva: str) -> None:
        if id_reserva not in self._reservas:
            self._reservas.append(id_reserva)

    def obtener_info(self) -> str:
        return f"Cliente[{self.id}] - {self.nombre} | {self.email} | Tel: {self.telefono}"

    def validar(self) -> bool:
        """Revalida el cliente (útil después de modificaciones futuras)."""
        try:
            self._validar_datos(self.nombre, self.email, self.telefono)
            return True
        except ClienteInvalidoError:
            return False

    def __str__(self) -> str:
        return self.obtener_info()
