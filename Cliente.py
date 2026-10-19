
import socket
import json

class Cliente:
    def __init__(self, host="localhost", port=8000):
        self.host = host
        self.port = port
        self.socket = None

    def conectar(self):
        try:
            self.socket = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.socket.connect((self.host, self.port))
            print(f"Conectado ao servidor {self.host}:{self.port}")

        except ConnectionRefusedError:
            print("Conexão recusada. Verifique se o servidor está ativo.")
            self.socket = None

        except OSError as erro:
            print(f"Erro de conexão: {erro}")
            self.socket = None
    def enviar(self, mensagem):
        if self.socket is None:
            print("Cliente não conectado.")
            return

        try:
            mensagem_json = json.dumps(mensagem, ensure_ascii=False)
            self.socket.sendall(mensagem_json.encode("utf-8"))

        except (OSError, TypeError, ValueError) as erro:
            print(f"Erro na comunicação: {erro}")

    def fechar(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None
            print("Conexão encerrada.")


if __name__ == "__main__":
    cliente = Cliente("localhost", 8000)

    cliente.conectar()

    if cliente.socket is not None:
        try:
            while True:
                mensagem = input("Digite uma mensagem (sair para encerrar): ")
                prioridade = input("Digite a prioridade (0 para alta, 1 para baixa): ")
                if mensagem.lower() == "sair":
                    break

                cliente.enviar({
                    "mensagem": mensagem,
                    "prioridade": int(prioridade)})

        finally:
            cliente.fechar()
