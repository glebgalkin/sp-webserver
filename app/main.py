import socket
from app.socket_handler import SocketHandler

def main():
    server_socket = None
    try:
        server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
        while True:
            client_socket, _ = server_socket.accept()
            print('New socket connection is created: ', client_socket)
            with SocketHandler(client_socket) as sh:
                sh.handle_request()

    except KeyboardInterrupt:
        print('Ctr + c command was triggered, shutting down...')
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
    finally:
        if server_socket:
            server_socket.close()
        print("Server has been shut down.")

main()