INFORME FINAL – SISTEMA DE GESTIÓN DE VACACIONES
APEX AMERICA

Asignatura: Programación II

1. Introducción

El presente trabajo consiste en el desarrollo de un sistema de gestión de vacaciones para la empresa Apex America, realizado utilizando el lenguaje de programación Python.

El objetivo principal es desarrollar una aplicación que permita administrar las solicitudes de vacaciones de los colaboradores, teniendo en cuenta sus preferencias de fechas, su situación familiar y los distintos niveles jerárquicos de la organización.

El sistema busca organizar el proceso de solicitud, evaluación, aprobación y confirmación de licencias, permitiendo una gestión más ordenada y transparente.

2. Objetivos del proyecto

Los principales objetivos del sistema son:

Administrar los datos personales y laborales de los colaboradores.
Permitir el inicio y cierre de sesión de los usuarios.
Registrar las solicitudes de vacaciones.
Asignar preferencias a las fechas solicitadas.
Establecer prioridades según la situación familiar.
Permitir que los supervisores evalúen las solicitudes.
Permitir que el área de Recursos Humanos confirme las licencias aprobadas.
Organizar las licencias mediante un algoritmo de ordenamiento.
Controlar la disponibilidad de días en los calendarios corporativos.
3. Estructura del sistema

El proyecto se organizó en diferentes módulos para separar las responsabilidades y facilitar su mantenimiento.

3.1. Módulo Models – Clases

En este módulo se desarrollaron las principales clases del sistema:

Colaborador: representa a los empleados de la empresa. Contiene información personal, laboral, credenciales de acceso y un historial de licencias. También calcula automáticamente la prioridad familiar.

Supervisor: hereda de la clase Colaborador y tiene la responsabilidad de aprobar o rechazar las solicitudes de vacaciones que cumplen con las condiciones establecidas.

AdministradorRRHH: también hereda de Colaborador y permite confirmar o rechazar las licencias que previamente fueron aprobadas y firmadas.

Licencia: representa cada solicitud de vacaciones. Contiene fechas de inicio y finalización, estado, tipo de licencia y nivel de preferencia. También permite validar el período y calcular la cantidad de días solicitados.

CalendarioCorporativo: administra los días disponibles por área e incorpora las licencias confirmadas, descontando los días correspondientes.

3.2. Módulo Service – Casos de uso

En este módulo se desarrolló la clase SistemaVacacionesApex, encargada de coordinar el funcionamiento general de la aplicación.

Entre sus principales funcionalidades se encuentran:

CU N.º 1: inicio y cierre de sesión.
CU N.º 4: asignación de preferencias a las fechas solicitadas.
CU N.º 6: firma de licencias asignadas por parte del colaborador.
CU N.º 10: alta de nuevos colaboradores.

Además, se incorporaron acciones específicas para supervisores y administradores de Recursos Humanos, permitiendo gestionar las distintas etapas de aprobación de las licencias.

El sistema también contempla el control de intentos fallidos de inicio de sesión, inhabilitando al usuario luego de tres intentos incorrectos.

3.3. Módulo Estructuras – Algoritmo de ordenamiento

Para organizar las solicitudes de vacaciones se implementó el algoritmo Merge Sort.

Este algoritmo permite ordenar las licencias considerando dos criterios:

Prioridad familiar en orden descendente.
Preferencia de fechas en orden ascendente.

La prioridad familiar se determina de la siguiente manera:

Colaborador casado: prioridad 3.
Colaborador con hijos: prioridad 1.
Colaborador sin hijos y soltero: prioridad 0.

En caso de coincidir ambos criterios, se conserva el orden original de las solicitudes.

Merge Sort utiliza la técnica de dividir y conquistar, separando la lista en partes más pequeñas, ordenándolas y luego combinándolas.

Su complejidad temporal es O(n log n) y su complejidad espacial es O(n).

3.4. Menú principal

Se desarrolló un menú interactivo por consola que permite utilizar el sistema mediante distintas opciones.

Las opciones disponibles dependen del tipo de usuario que haya iniciado sesión.

Los colaboradores pueden rankear sus fechas y firmar las licencias asignadas.

Los supervisores pueden aprobar o rechazar solicitudes de su área y consultar las licencias ordenadas.

Los administradores de Recursos Humanos pueden confirmar o rechazar licencias aprobadas, dar de alta nuevos colaboradores y consultar las solicitudes ordenadas.

Esta separación permite que cada usuario acceda únicamente a las funcionalidades correspondientes a su rol.

4. Proceso de gestión de vacaciones

El funcionamiento general del sistema sigue las siguientes etapas:

El colaborador inicia sesión.
Consulta sus solicitudes de vacaciones.
Asigna un nivel de preferencia a las fechas solicitadas.
Las solicitudes pueden organizarse mediante Merge Sort, considerando la prioridad familiar y las preferencias.
El supervisor evalúa las solicitudes y decide aprobarlas o rechazarlas.
Si el supervisor aprueba una solicitud, esta pasa al estado asignada.
El colaborador firma la licencia y su estado cambia a aprobada.
El administrador de Recursos Humanos confirma o rechaza la licencia.
Una licencia confirmada puede incorporarse al calendario corporativo, descontando los días correspondientes.

Los estados utilizados en el sistema son: pendiente, asignada, aprobada, confirmada y rechazada.

5. Validaciones implementadas

Para mejorar la confiabilidad del sistema se incorporaron diferentes controles:

Validación de fechas de ingreso.
Control de legajos y DNI positivos.
Verificación de credenciales obligatorias.
Validación de estados permitidos para las licencias.
Control de preferencias entre los valores 1 y 3.
Verificación de que una licencia pertenezca al colaborador correspondiente.
Control de duplicados en los historiales.
Validación de los períodos de vacaciones.
Control de disponibilidad de días en los calendarios.
Restricción de funcionalidades según el rol del usuario.
Control de intentos fallidos de inicio de sesión.

También se utilizaron excepciones como ValueError, TypeError, PermissionError y LookupError para informar situaciones incorrectas durante la ejecución.

6. Pruebas unitarias

Se desarrolló un módulo de pruebas utilizando la biblioteca unittest de Python.

Se plantearon nueve pruebas unitarias:

Pruebas de clases (5):

Verificación del cálculo de prioridad familiar de los colaboradores.
Comprobación del funcionamiento de la clase Supervisor.
Comprobación del funcionamiento de AdministradorRRHH.
Validación de los períodos de las licencias.
Verificación de la incorporación de vacaciones al calendario corporativo.

Pruebas de casos de uso (4):

Verificación del inicio de sesión.
Comprobación de la asignación de preferencias y el ordenamiento de licencias.
Verificación de la firma de una licencia.
Comprobación del alta de nuevos colaboradores.

Estas pruebas permiten comprobar el comportamiento de las principales funcionalidades y detectar posibles errores durante el desarrollo.

7. Herramientas y tecnologías utilizadas

Para desarrollar el proyecto se utilizaron:

Python: lenguaje de programación principal.
Programación orientada a objetos: implementación de clases, atributos, métodos, herencia y encapsulamiento de responsabilidades.
Merge Sort: algoritmo de ordenamiento de solicitudes.
Unittest: biblioteca utilizada para realizar pruebas unitarias.
Visual Studio Code: entorno de desarrollo utilizado para escribir y ejecutar el código.
8. Conclusión

A través de este proyecto se logró desarrollar un sistema de gestión de vacaciones que integra diferentes conceptos de programación estudiados durante la asignatura.

Se aplicaron principios de programación orientada a objetos mediante la creación de clases y relaciones de herencia, se implementaron casos de uso para representar las operaciones principales del sistema y se utilizó el algoritmo Merge Sort para organizar las solicitudes según criterios de prioridad.

Además, la incorporación de validaciones y pruebas unitarias permitió mejorar la organización y confiabilidad del programa.

Como resultado, se obtuvo una aplicación que permite administrar las solicitudes de vacaciones de manera estructurada, diferenciando las responsabilidades de colaboradores, supervisores y administradores de Recursos Humanos.

El desarrollo permitió integrar los conocimientos de la materia en una situación práctica, representando un proceso de gestión real dentro de una organización.