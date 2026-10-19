import socket
class Worker:
    def __init__(self, host="localhost", port=8001):
        self.host = host
        self.port = port
        
    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"Worker ouvindo em {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Conexão estabelecida com {addr}")
                    data = conn.recv(1024)

                    if not data:
                        break

                    mensagem = data.decode("utf-8")
                    print(f"Recebido do servidor: {mensagem}")

                    # Aqui você pode processar a mensagem recebida
                    # Por exemplo, você pode chamar a função de validação de URL

if __name__ == "__main__":
    worker = Worker()
    worker.start()
    