# Comunicación Cifrada Cliente-Servidor con RSA

Este proyecto contiene un ejemplo de cómo establecer una comunicación cifrada entre un cliente y un servidor utilizando el algoritmo de cifrado RSA. El servidor genera un par de claves RSA y envía su clave pública al cliente. El cliente genera su propio par de claves RSA y envía su clave pública al servidor. Luego, el cliente cifra un mensaje con la clave pública del servidor y envía el mensaje cifrado. El servidor descifra el mensaje con su clave privada, y opcionalmente, puede enviar una respuesta cifrada de vuelta al cliente.

## Requisitos

- Python 3.x
- Biblioteca `cryptography`

## Instalación

1. Clona este repositorio o descarga los archivos `servidor.py` y `cliente.py`.
2. Instala la biblioteca `cryptography` ejecutando el siguiente comando:
"pip install cryptography"

## Uso
1. Ejecuta el script del servidor:
"python servidor.py"

El servidor comenzará a escuchar en el puerto 3000 y mostrará un mensaje indicando que está listo para aceptar conexiones.

2. En otra terminal o ventana de comandos, ejecuta el script del cliente:
"python cliente.py"

El cliente se conectará al servidor, intercambiará claves públicas y enviará un mensaje cifrado al servidor. El servidor descifra el mensaje y lo muestra en la consola.

3. Opcionalmente, el servidor puede enviar una respuesta cifrada de vuelta al cliente.

## Detalles de implementación

- El servidor genera un par de claves RSA de 4096 bits.
- El cliente también genera un par de claves RSA de 4096 bits.
- El servidor envía su clave pública al cliente.
- El cliente envía su clave pública al servidor.
- El cliente cifra un mensaje con la clave pública del servidor utilizando el algoritmo de relleno OAEP y el hash SHA-256.
- El servidor descifra el mensaje con su clave privada utilizando el mismo algoritmo de relleno y hash.
- Opcionalmente, el servidor puede cifrar una respuesta con la clave pública del cliente y enviarla de vuelta.

## Nota

Este código es un ejemplo básico y no debe usarse en un entorno de producción sin una revisión y pruebas adicionales. Además, asegúrate de manejar adecuadamente los casos de error y las conexiones perdidas.