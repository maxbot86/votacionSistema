# votacionSistema - Proyecto Web con Docker y Flask

Este proyecto es una aplicación web que utiliza Docker para inicializar varios servicios, incluyendo una aplicación web con Flask y una base de datos ( SQLITE en primera instancia pero con la estructura para migrar a otra mas robusta).

## Instrucciones para Inicializar el Docker Compose

Para ejecutar el proyecto en tu entorno local utilizando Docker Compose, sigue los siguientes pasos:

1. Asegúrate de tener Docker instalado en tu máquina.
2. Navega hasta el directorio del proyecto donde se encuentra el archivo `docker-compose.yml`.
3. Ejecuta el siguiente comando para inicializar el Docker Compose con la opción de `--build`, lo que asegurará que las imágenes se construyan correctamente.

```bash
docker compose up --build
```


## Acceso a la Aplicación Web

Una vez que los contenedores estén corriendo, puedes acceder a la aplicación web mediante el siguiente enlace:

http://localhost:8080

Este enlace te llevará a la página principal de la aplicación que se está ejecutando en el contenedor.


## Manual de Usuario
Dentro del repositorio se incluye un manual de usuario que detalla el uso de la aplicación y sus funcionalidades. Puedes encontrar el documento en el siguiente archivo:

MM - Manual de usuario - V01.docx

Este manual contiene información detallada sobre cómo utilizar la aplicación web.


## IOT
Dentro del repositorio ademas se incluye una carpeta con el codigo para la implementacion de un controlador ESP8266 como dispositivo de votacion. Este constara de 3 botones, cada uno con su id asignado que enviara mediante POST a el endpoint para sumar 1 voto a la lista definida.
Dentro del codigo solo falta definir el SSID del WIFI y la CLAVE para que el mismotenga acceso a la red. Ademas se puede parametrisar el ENDPOINT dependiendo de donde se aloje y via que DNS se dese acceder. 
