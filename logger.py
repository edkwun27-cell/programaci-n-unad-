"""
Sistema Integral de Gestión de Clientes, Servicios y Reservas - Software FJ
Curso: Programación 213023 - UNAD
Archivo: logger.py
Descripción: Configuración centralizada de logging a archivo.
"""

import logging
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).parent / "logs.txt"

def configurar_logger() -> logging.Logger:
    """Configura y retorna el logger del sistema."""
    logger = logging.getLogger("SoftwareFJ")
    logger.setLevel(logging.INFO)
    
    # Evitar duplicados
    if logger.handlers:
        return logger
    
    # Formato
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Handler de archivo
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # También consola (opcional, útil para demo)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logger.info("=== Sistema Software FJ iniciado ===")
    return logger

# Instancia global
logger = configurar_logger()
