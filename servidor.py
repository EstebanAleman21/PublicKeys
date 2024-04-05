import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Generar un par de claves RSA de 4096 bits
private_key = rsa.generate_private_key(
    public_exponent=65537,  # Exponente público comúnmente utilizado en RSA
    key_size=4096           # Longitud de la clave RSA en bits
)
public_key = private_key.public_key()  # Obtiene la clave pública correspondiente

# Crear un socket TCP
HOST = '127.0.0.1'  # Dirección IP del servidor
PORT = 3000         # Puerto en el que el servidor escucha las conexiones entrantes

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))  # Enlaza el socket a la dirección y puerto especificados
    server_socket.listen()            # Escucha las conexiones entrantes

    print("Servidor escuchando en el puerto", PORT)

    while True:
        # Aceptar conexiones entrantes
        conn, addr = server_socket.accept()
        print('Cliente conectado:', addr)

        # Enviar la clave pública al cliente
        conn.sendall(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,  # Formato de codificación (PEM)
            format=serialization.PublicFormat.SubjectPublicKeyInfo  # Formato de la clave pública
        ))

        # Recibir datos del cliente
        data = conn.recv(4096)
        client_public_key = serialization.load_pem_public_key(data)  # Cargar la clave pública del cliente

        # Recibir el mensaje cifrado del cliente
        cipher_text = conn.recv(4096)

        # Descifrar el mensaje cifrado con la clave privada del servidor
        decrypted_data = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Algoritmo de generación de máscaras
                algorithm=hashes.SHA256(),  # Algoritmo de hash
                label=None  # Datos opcionales para la operación de cifrado
            )
        )

        # Mostrar los datos descifrados
        print('Datos descifrados:', decrypted_data.decode())

        # Enviar una respuesta al cliente (opcional)
        response = b'Mensaje recibido correctamente'
        conn.sendall(client_public_key.encrypt(
            response,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),  # Algoritmo de generación de máscaras
                algorithm=hashes.SHA256(),  # Algoritmo de hash
                label=None  # Datos opcionales para la operación de cifrado
            )
        ))

        # Cerrar la conexión con el cliente
        conn.close()
