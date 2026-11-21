# Sistema Integral de Gestión de Clientes, Servicios y Reservas
## Software FJ - Componente Práctico Fase 4

**Curso:** Programación (Código 213023)  
**Universidad:** Universidad Nacional Abierta y a Distancia (UNAD)  
**Programa:** Ingeniería de Sistemas  

### Descripción

Sistema orientado a objetos desarrollado en Python para la gestión de clientes, servicios (reservas de salas, alquiler de equipos y asesorías especializadas) y reservas de la empresa ficticia **Software FJ**.

El sistema implementa rigurosamente los principios de:
- Abstracción
- Herencia
- Polimorfismo
- Encapsulación
- Manejo avanzado de excepciones

**No utiliza bases de datos.** Toda la gestión se realiza en memoria mediante objetos y listas. Los archivos se usan únicamente para el registro de eventos y errores (`logs.txt`).

### Características principales

- Clase abstracta `Entidad` como base.
- Clase `Cliente` con validaciones robustas y encapsulación.
- Clase abstracta `Servicio` + 3 implementaciones concretas:
  - `ReservaSala`
  - `AlquilerEquipo`
  - `AsesoriaEspecializada`
- Clase `Reserva` con confirmación, cancelación y procesamiento.
- Métodos sobrecargados (cálculo de costos con/sin impuestos y descuentos).
- Excepciones personalizadas + bloques `try/except`, `try/except/else`, `try/except/finally` y encadenamiento de excepciones.
- Logging completo de errores y eventos.
- Simulación de más de 10 operaciones (válidas e inválidas) demostrando estabilidad del sistema.

### Estructura del proyecto

```
SoftwareFJ/
├── exceptions.py      # Excepciones personalizadas
├── logger.py          # Configuración de logging
├── entidad.py         # Clase abstracta base
├── cliente.py         # Clase Cliente
├── servicio.py        # Servicio abstracto + 3 servicios especializados
├── reserva.py         # Clase Reserva
├── gestor.py          # Gestor del sistema (listas en memoria)
├── main.py            # Simulación / demostración
└── logs.txt           # Generado al ejecutar (registro de eventos)
```

### Cómo ejecutar

```bash
cd SoftwareFJ
python main.py
```

El sistema ejecutará una secuencia de operaciones y generará el archivo `logs.txt`.

### Evidencias requeridas

- Repositorio en GitHub con este código.
- Documento PDF con: Portada, Introducción, Enlace del repositorio, Conclusiones y Referencias APA.

---
*Proyecto desarrollado para el componente práctico del curso Programación 213023.*
