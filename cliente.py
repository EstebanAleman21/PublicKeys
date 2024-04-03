import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Crear un socket TCP
HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    print('Conectado al servidor')

    # Recibir la clave pública del servidor
    server_public_key_pem = client_socket.recv(4096)
    server_public_key = serialization.load_pem_public_key(server_public_key_pem)

    # Generar un par de claves RSA de 4096 bits para el cliente
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096
    )
    public_key = private_key.public_key()

    # Enviar la clave pública del cliente al servidor
    client_socket.sendall(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    # Mensaje a enviar al servidor
    message = b'Hola, servidor' * 10  # Mensaje de 1200 bytes

    # Cifrar el mensaje con la clave pública del servidor
    cipher_text = server_public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Enviar el mensaje cifrado al servidor
    client_socket.sendall(cipher_text)

    # Recibir y descifrar la respuesta del servidor
    response_cipher_text = client_socket.recv(4096)
    decrypted_response = private_key.decrypt(
        response_cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    print('Respuesta del servidor:', decrypted_response.decode())

    client_socket.close()