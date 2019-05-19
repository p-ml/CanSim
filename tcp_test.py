import socket


def server():
    host = socket.gethostname()
    port = 12345

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))

        s.listen(1)

        c, address = s.accept()
        print("Connection from: " + str(address))

        while True:
            data = c.recv(1024).decode('utf-8')

            if not data:
                break

            print(data)

        c.close()


if __name__ == '__main__':
    server()
