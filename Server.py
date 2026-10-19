import json
import socket
import threading
from utils.URLValiidator import URLValidator


class Server:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.validator = URLValidator()
        self.fila = []
        self.lock = threading.Lock()

    def handle_client(self, conn, addr):
        with conn:
            print(f"Cliente conectado: {addr}")

            try:
                while True:
                    data = conn.recv(1024)

                    if not data:
                        break

                    mensagem = data.decode("utf-8")
                    print(f"Recebido do cliente {addr}: {mensagem}")

                    mensagem = json.loads(mensagem)

                    resultado = self.validator.verificar(
                        mensagem["mensagem"],
                        mensagem["prioridade"]
                    )

                    # Adiciona à fila com acesso protegido
                    with self.lock:
                        self.fila.append(
                            (resultado["prioridade"], resultado)
                        )

                    print(f"URL adicionada à fila: {resultado['url']}")

            except (ConnectionError, json.JSONDecodeError, KeyError) as erro:
                print(f"Erro com o cliente {addr}: {erro}")

            finally:
                print(f"Cliente desconectado: {addr}")

    
    def processar_fila(self):
        while True:
            with self.lock:
                if self.fila:
                    # Ordena a fila por prioridade (0 = alta, 1 = baixa)
                    self.fila.sort(key=lambda x: x[0])
                    prioridade, resultado = self.fila.pop(0)
                    self.conectar_worker(resultado)
                    
    def conectar_worker(self,json_data):
        try:
            self.socket_worker = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.socket_worker.connect(("localhost", 8001))

            print("Conectado ao worker em localhost:8001")
            
            self.socket_worker.sendall(json.dumps(json_data).encode("utf-8"))
            return True

        except OSError as erro:
            print(f"Erro ao conectar com o worker: {erro}")
            self.socket_worker = None
            return False
                    
                    
                    
                                        

    def start(self):
        # Thread dedicada ao processamento da fila
        threading.Thread(
            target=self.processar_fila,
            daemon=True
        ).start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.port))
            s.listen()

            print(f"Servidor ouvindo em {self.host}:{self.port}")

            while True:
                conn, addr = s.accept()

                thread = threading.Thread(
                    target=self.handle_client,
                    args=(conn, addr),
                    daemon=True
                )
                thread.start()


if __name__ == "__main__":
    server = Server()
    server.start()