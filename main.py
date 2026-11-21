"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: main.py
Descripción: Simulación de al menos 10 operaciones completas (válidas e inválidas).
Demuestra el manejo robusto de excepciones: try/except, try/except/else, try/except/finally,
encadenamiento de excepciones, y continuidad del sistema ante errores.
"""

from gestor import GestorSistema
from servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from exceptions import (
    ClienteInvalidoError,
    ServicioInvalidoError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ParametrosInvalidosError
)
from logger import logger


def ejecutar_operacion(descripcion: str, funcion, *args, **kwargs):
    """
    Wrapper para ejecutar operaciones con manejo de excepciones profesional.
    Usa try/except/else/finally y registra todo.
    """
    print(f"\n--- Operación: {descripcion} ---")
    resultado = None
    try:
        resultado = funcion(*args, **kwargs)
    except (ClienteInvalidoError, ServicioInvalidoError, ReservaInvalidaError,
            OperacionNoPermitidaError, ParametrosInvalidosError) as e:
        logger.error(f"Error controlado en '{descripcion}': {e}")
        print(f"ERROR CONTROLADO: {e}")
        # Encadenamiento explícito en algunos casos
        if hasattr(e, '__cause__') and e.__cause__:
            print(f"  Causa original: {e.__cause__}")
    except Exception as e:
        logger.critical(f"Error inesperado en '{descripcion}': {e}")
        print(f"ERROR INESPERADO: {e}")
    else:
        logger.info(f"Operación exitosa: {descripcion}")
        print(f"ÉXITO: {resultado if resultado else 'Operación completada'}")
    finally:
        logger.info(f"Finalizada operación: {descripcion}")
        print(f"--- Fin de: {descripcion} ---\n")
    return resultado


def main():
    print("=" * 70)
    print("   SISTEMA INTEGRAL DE GESTIÓN - SOFTWARE FJ")
    print("   Curso: Programación 213023 - UNAD")
    print("   Demostración de POO + Manejo Avanzado de Excepciones")
    print("=" * 70)

    gestor = GestorSistema()

    # ==================== REGISTRO DE CLIENTES ====================
    # 1. Cliente válido
    ejecutar_operacion(
        "Registrar cliente válido",
        gestor.registrar_cliente,
        "C001", "Juan Pérez", "juan.perez@email.com", "3001234567"
    )

    # 2. Cliente con email inválido
    ejecutar_operacion(
        "Registrar cliente con email inválido",
        gestor.registrar_cliente,
        "C002", "Ana Gómez", "ana-email-invalido", "3109876543"
    )

    # 3. Cliente con nombre muy corto
    ejecutar_operacion(
        "Registrar cliente con nombre corto",
        gestor.registrar_cliente,
        "C003", "Al", "al@email.com", "3155555555"
    )

    # 4. Otro cliente válido
    ejecutar_operacion(
        "Registrar segundo cliente válido",
        gestor.registrar_cliente,
        "C004", "María López", "maria.lopez@empresa.com", "3201112233"
    )

    # ==================== REGISTRO DE SERVICIOS ====================
    # 5. Servicio Sala válido
    sala = ReservaSala("S001", "Sala Ejecutiva Norte", 80.0, 12, "Piso 3")
    ejecutar_operacion("Registrar servicio Sala válida", gestor.registrar_servicio, sala)

    # 6. Servicio Alquiler válido
    equipo = AlquilerEquipo("S002", "Laptop Dell XPS", 25.0, "Laptop", 5)
    ejecutar_operacion("Registrar servicio Alquiler de equipo", gestor.registrar_servicio, equipo)

    # 7. Servicio Asesoría válida
    asesoria = AsesoriaEspecializada("S003", "Consultoría en Arquitectura de Software", 120.0, "avanzado", "Ing. Carlos Ruiz")
    ejecutar_operacion("Registrar servicio Asesoría especializada", gestor.registrar_servicio, asesoria)

    # 8. Intento de servicio inválido (capacidad negativa)
    try:
        sala_mala = ReservaSala("S004", "Sala Invalida", 50.0, -5, "Sótano")
        gestor.registrar_servicio(sala_mala)
    except ServicioInvalidoError as e:
        logger.error(f"Servicio inválido capturado: {e}")
        print(f"ERROR CONTROLADO (servicio): {e}")

    # ==================== CREACIÓN DE RESERVAS ====================
    # 9. Reserva válida
    ejecutar_operacion(
        "Crear reserva válida de sala",
        gestor.crear_reserva,
        "R001", "C001", "S001", 3.0
    )

    # 10. Reserva con cliente inexistente
    ejecutar_operacion(
        "Crear reserva con cliente inexistente",
        gestor.crear_reserva,
        "R002", "C999", "S002", 2.0
    )

    # 11. Reserva con duración inválida
    ejecutar_operacion(
        "Crear reserva con duración negativa",
        gestor.crear_reserva,
        "R003", "C004", "S003", -1.5
    )

    # 12. Segunda reserva válida
    ejecutar_operacion(
        "Crear reserva de asesoría",
        gestor.crear_reserva,
        "R004", "C004", "S003", 2.0
    )

    # ==================== PROCESAMIENTO DE RESERVAS ====================
    # 13. Confirmar y procesar reserva
    reserva1 = gestor.obtener_reserva("R001")
    if reserva1:
        ejecutar_operacion("Confirmar reserva R001", reserva1.confirmar)
        ejecutar_operacion(
            "Procesar reserva R001 con impuestos y descuento",
            reserva1.procesar,
            aplicar_impuesto=True,
            descuento=0.10
        )

    # 14. Intentar cancelar reserva ya procesada
    if reserva1:
        ejecutar_operacion("Intentar cancelar reserva ya procesada", reserva1.cancelar, "Cambio de planes")

    # 15. Procesar segunda reserva sin impuestos
    reserva4 = gestor.obtener_reserva("R004")
    if reserva4:
        ejecutar_operacion("Procesar reserva R004 sin impuestos", reserva4.procesar, aplicar_impuesto=False)

    # ==================== RESUMEN FINAL ====================
    print("\n" + "=" * 70)
    print("RESUMEN FINAL DEL SISTEMA")
    print("=" * 70)
    print(gestor.resumen())
    print("\nClientes registrados:")
    for c in gestor.listar_clientes():
        print(f"  - {c}")
    print("\nServicios disponibles:")
    for s in gestor.listar_servicios():
        print(f"  - {s}")
        print(f"    Descripción: {s.describir()}")
    print("\nReservas:")
    for r in gestor.listar_reservas():
        print(f"  - {r}")

    print("\n" + "=" * 70)
    print("Simulación finalizada. El sistema permaneció estable ante todos los errores.")
    print(f"Todos los eventos y errores fueron registrados en: logs.txt")
    print("=" * 70)
    logger.info("=== Simulación completada exitosamente ===")


if __name__ == "__main__":
    main()
