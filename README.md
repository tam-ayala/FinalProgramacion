Trabajo Final Integrador para la asignatura **Programación II** (Tecnicatura Superior en Desarrollo de Software - Instituto Técnico Superior Córdoba).

El proyecto es un prototipo funcional en Python basado en el modelado del flujo de **Solicitud y Rankeo de Vacaciones** para la empresa **Apex América**
 Características del Sistema

- **Modelado de Clases**: Implementación de las clases principales del dominio (`Colaborador`, `Supervisor`, `AdministradorRRHH`, `Licencia`).
- **Casos de Uso**:
  - `CU N1`: Autenticación e inicio de sesión (Login).
  - `CU N4`: Rankeo de fechas de vacaciones.
  - `CU N6`: Firma de licencias en conformidad.
  - `CU N10`: Alta de nuevos colaboradores por el Administrador de RRHH.
- **Algoritmo de Ordenamiento**: Ordenamiento por el método **Bubble Sort** para priorizar las fechas candidatas según la preferencia asignada por el usuario (Prioridad 1 a 3).
- **Interfaz Interactiva**: Menú por consola accesible para probar las distintas funcionalidades.
- **Pruebas Unitarias**: Suite de pruebas con `unittest` que valida cada clase y caso de uso.

---

Estructura del Proyecto

.
├── clases.py                   # Modelos de dominio (Colaborador, Licencia, etc.)
├── casos_uso.py                # Lógica del sistema y casos de uso
├── algoritmo_ordenamiento.py   # Implementación del algoritmo Bubble Sort
├── test_sistema.py             # Pruebas unitarias de clases y casos de uso
├── main.py                     # Menú interactivo principal
└── README.md                   