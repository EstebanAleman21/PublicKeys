import socket
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes

# Generar un par de claves RSA de 4096 bits
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096
)
public_key = private_key.public_key()

# Crear un socket TCP
HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print("Servidor escuchando en el puerto", PORT)

    while True:
        conn, addr = server_socket.accept()
        print('Cliente conectado:', addr)

        # Enviar la clave pública al cliente
        conn.sendall(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

        # Recibir datos del cliente
        data = conn.recv(4096)
        client_public_key = serialization.load_pem_public_key(data)

        # Recibir el mensaje cifrado del cliente
        cipher_text = conn.recv(4096)

        # Descifrar el mensaje cifrado con la clave privada del servidor
        decrypted_data = private_key.decrypt(
            cipher_text,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        print('Datos descifrados:', decrypted_data.decode())

        # Enviar una respuesta al cliente (opcional)
        response = b'Mensaje recibido correctamente'
        conn.sendall(client_public_key.encrypt(
            response,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ))

        conn.close()