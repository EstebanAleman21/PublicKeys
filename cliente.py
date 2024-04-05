import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Crear un socket TCP
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 3000         # Puerto en el que el servidor escucha las conexiones entrantes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))  # Conectar al servidor en la dirección y puerto especificados
    print('Conectado al servidor')

    # Recibir la clave pública del servidor
    server_public_key_pem = client_socket.recv(4096)  # Recibe la clave pública del servidor en formato PEM
    server_public_key = serialization.load_pem_public_key(server_public_key_pem)  # Cargar la clave pública del servidor

    # Generar un par de claves RSA de 4096 bits para el cliente
    private_key = rsa.generate_private_key(
        public_exponent=65537,  # Exponente público comúnmente utilizado en RSA
        key_size=4096           # Longitud de la clave RSA en bits
    )
    public_key = private_key.public_key()  # Obtiene la clave pública correspondiente

    # Enviar la clave pública del cliente al servidor
    client_socket.sendall(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,  # Formato de codificación (PEM)
        format=serialization.PublicFormat.SubjectPublicKeyInfo  # Formato de la clave pública
    ))

    # Mensaje a enviar al servidor
    message = b'Hola, servidor' * 10  # Mensaje de 1200 bytes

    # Cifrar el mensaje con la clave pública del servidor
    cipher_text = server_public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Algoritmo de generación de máscaras
            algorithm=hashes.SHA256(),  # Algoritmo de hash
            label=None  # Datos opcionales para la operación de cifrado
        )
    )

    # Enviar el mensaje cifrado al servidor
    client_socket.sendall(cipher_text)

    # Recibir y descifrar la respuesta del servidor
    response_cipher_text = client_socket.recv(4096)  # Recibe la respuesta cifrada del servidor
    decrypted_response = private_key.decrypt(  # Descifra la respuesta usando la clave privada del cliente
        response_cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Algoritmo de generación de máscaras
            algorithm=hashes.SHA256(),  # Algoritmo de hash
            label=None  # Datos opcionales para la operación de cifrado
        )
    )

    print('Respuesta del servidor:', decrypted_response.decode())  # Imprime la respuesta descifrada

    client_socket.close()  # Cierra la conexión con el servidor