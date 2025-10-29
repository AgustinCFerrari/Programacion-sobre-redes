# Práctica Formativa: Rediseño de Sistema Distribuido (Cliente-Servidor)

## Descripción General
Este proyecto ilustra cómo transformar una aplicación monolítica en un sistema distribuido **Cliente-Servidor**, utilizando componentes como **balanceo de carga (NGINX)**, **colas de mensajes (RabbitMQ)** y **persistencia** en base de datos con **SQLite3**. El sistema está compuesto por:

- **Cliente Python**
- **Servidor principal** con threading y RabbitMQ
- **Workers** consumidores multihilo
- **Balanceador NGINX**
- **Monitor de tareas**
- **Diagrama arquitectónico**

## Requerimientos
- **Python 3.x**
- **RabbitMQ** funcionando localmente (`localhost`)
- **NGINX** instalado y configurado como balanceador de carga
- **Módulos Python**: `pika`, `sqlite3`
- **Base de datos**: SQLite3 utilizada como almacenamiento persistente (archivo local `resultados.db`)
- **Sistema operativo** compatible: Linux / Windows / macOS

## Arquitectura del Sistema
```
Cliente (client.py)
     |
     v
Balanceador de carga (nginx.conf)
     |
     v
Servidor Principal (recibe tareas y las envía a RabbitMQ)
     |
     v
RabbitMQ (cola de mensajes)
     |
     v
Workers (worker.py, procesan tareas y guardan resultado en SQLite3)
     |
     v
Monitor (monitor.py, muestra tareas procesadas en tiempo real)
```
> Ver **Diagrama.txt** para la representación visual.

## Detalle de los Archivos

### 1. `client.py`
**Función:** Actúa como el cliente que envía tareas al servidor a través de un socket TCP. Permite al usuario ingresar tareas que luego se transmiten al servidor para su procesamiento.

### 2. `nginx.conf`
**Función:** Configuración de NGINX como balanceador de carga, distribuyendo las peticiones entrantes entre múltiples instancias del servidor principal.

### 3. `worker.py`
**Función:** Worker que consume tareas de RabbitMQ, las procesa en hilos independientes y **almacena el resultado en la base de datos SQLite3**. Simula el procesamiento de cada tarea y registra el resultado final.  
**Base de datos:** El archivo `resultados.db` creado con SQLite3 almacena cada tarea procesada junto con su resultado.

### 4. `monitor.py`
**Función:** Monitoriza la base de datos SQLite3, mostrando en tiempo real las tareas que han sido procesadas y almacenadas por los workers. Refresca cada segundo la pantalla y lista los resultados.

### 5. `Diagrama.txt`
**Función:** Contiene el diagrama textual de la arquitectura distribuida del sistema, mostrando el flujo desde el cliente hasta la persistencia del resultado.

## Ejecución Paso a Paso

1. **Levantar RabbitMQ y NGINX** según la configuración de `nginx.conf`.
2. **Iniciar workers** ejecutando `worker.py` (pueden ser varios en paralelo para aprovechar el balanceo y procesamiento multihilo).
3. **Ejecutar el monitor** para visualizar el procesamiento con `monitor.py`.
4. **Ejecutar el cliente** con `client.py`, ingresar tareas que serán procesadas y distribuidas por el sistema; cada tarea y su resultado se **almacenan automáticamente** en la base `SQLite3` (`resultados.db`).

## Notas Finales
- **SQLite3** es una base de datos local, ideal para **pruebas formativas** y entornos con pocos requerimientos de concurrencia.
- El archivo **`resultados.db`** será generado automáticamente en el directorio de ejecución.
- El diseño es **escalable**: pueden agregarse más **workers** y mejorar el balanceo añadiendo más servidores detrás de **NGINX**.
- Monitorear posibles **errores de conexión** en la comunicación **Cliente-Servidor** y en el **acceso a la base de datos**.
