import socket as s
import time as t
import logging as l
import threading as th
import hashlib as h
import pathlib as p
import os

NOME_DO_SERVER = ''
TAM_BUFFER = 2048
PORTA_DO_SERVER = 6000
ENDERECO_IP = (NOME_DO_SERVER, PORTA_DO_SERVER)

# Funções padrão --------------------------------------------

def titulo():
    print("--------------------")
    print("      SERVIDOR")
    print("--------------------\n")


def mensagem_envio(servidor_socket : s.socket, mensagem : str):
    servidor_socket.send(mensagem.encode())
    logger.info(f"Enviado:  '{mensagem}'")


def mensagem_recebimento(servidor_socket : s.socket):
    mensagem = servidor_socket.recv(TAM_BUFFER).decode('utf-8')
    logger.info(f"Recebido: '{mensagem}'")
    return mensagem


def chat_envio(servidor_socket : s.socket, mensagem : str):
    servidor_socket.send(mensagem.encode())
    print("--------------------")
    print('Enviado: ', mensagem)
    print("--------------------\n")
    

def chat_recebimento(servidor_socket : s.socket):
    mensagem = servidor_socket.recv(TAM_BUFFER).decode('utf-8')
    print(mensagem)
    print("--------------------\n")
    return mensagem
    

def iniciar_servidor():
    inicializar = ''
    iniciar_server = False
    while inicializar == '':
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        inicializar = input("Deseja inicializar o servidor [S/N] ? ").lower().strip()
        match inicializar:
            case 's':
                iniciar_server = True
            case 'sim':
                iniciar_server = True
            case 'n':
                iniciar_server = False
            case 'não':
                iniciar_server = False
            case _:
                print('A escolha precisa estar nas opções acima!')
                t.sleep(2)
                inicializar = ''
    return iniciar_server


def opcoes_cliente(conexao_socket:s.socket):
    opcao = 0
    cliente_opcao = mensagem_recebimento(conexao_socket).split("-")
    
    if cliente_opcao[0] == 'OPTION':
        opcao = int(cliente_opcao[1])
        
    match opcao:
        case 1:
            enviar_arquivo(conexao_socket)
        case 2:
            chat_servidor(conexao_socket)
        case 3:
            iniciar_server = False
            clientes.remove(conexao_socket)


def retornar_nome_arquivos(conexao_socket:s.socket):
    os.system('cls' if os.name == 'nt' else 'clear')

    caminho = str(p.Path.cwd()) + '\Arquivos'
    file_paths = os.listdir(caminho)
    num_arquivos = len(file_paths)

    mensagem_envio(conexao_socket, str(num_arquivos))
    
    confirmacao_tam = mensagem_recebimento(conexao_socket).split("-")
    
    if(confirmacao_tam[0] == "ERROR"):
        t.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        return
    else:
        for i in range(0, num_arquivos):
            mensagem_envio(conexao_socket, file_paths[i])
            
        while True:
            nome_arquivo = mensagem_recebimento(conexao_socket)
                
            if not os.path.exists(os.path.join("./Arquivos", nome_arquivo)):
                mensagem_envio(conexao_socket, "ERROR-3-Arquivo não encontrado!")
            else:
                mensagem_envio(conexao_socket, 'OK-1-Confirmação')
                break
        return nome_arquivo
    
    
def enviar_arquivo(conexao_socket:s.socket):
    nome_arquivo = retornar_nome_arquivos(conexao_socket)
    num_pacotes = (os.path.getsize(os.path.join("./Arquivos", nome_arquivo)) // TAM_BUFFER) + 1
    
    mensagem_envio(conexao_socket, f"OK-2-{num_pacotes}")
    with open(os.path.join("./Arquivos", nome_arquivo), "rb") as arquivo:
        i = 0
        while data := arquivo.read(TAM_BUFFER):
            conexao_socket.send(data)
            ack = mensagem_recebimento(conexao_socket).strip("-")
            if (ack[1] == str(num_pacotes)):
                print('Todos os pacotes foram mandados com sucesso!')
                t.sleep(2)
                break
            if (ack[1] == str(i+1)):
                i += 1
        

def receber_mensagem_servidor(server : s.socket):
    while True:
        try:
            msg = server.recv(TAM_BUFFER).decode('utf-8')
            print(msg)
            if(msg == "Sair"):
                break
        except:
            return


def enviar_mensagem_servidor(server : s.socket):
    while True:
        try:
            msg = input()
            server.send(f'<Servidor> {msg}'.encode('utf-8'))
        except:
            break


def chat_servidor(client : s.socket):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Chat SERVIDOR X CLIENTE")
    thread_receber_msg = th.Thread(target=receber_mensagem_servidor, args=[client])
    thread_enviar_msg = th.Thread(target=enviar_mensagem_servidor, args=[client])

    thread_receber_msg.start()
    thread_enviar_msg.start()


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    
    try:
        server_socket.bind(ENDERECO_IP)
        server_socket.listen()
        server_socket.settimeout(30)
    except:
        print('Não foi possível iniciar o servidor!')
        return

    iniciar_server = iniciar_servidor()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Esperando resposta')

    while iniciar_server:
        conexao_socket, endereco = server_socket.accept()
        clientes.append(conexao_socket)
        thread = th.Thread(target=opcoes_cliente, args=(conexao_socket,), daemon=True)
        thread.start()
        

if __name__ == "__main__":
    clientes = []
    iniciar_server = False
    
    logger = l.getLogger(__name__)
    l.basicConfig(filename="server.log", encoding="utf-8", level=l.INFO, format="%(levelname)s - %(asctime)s: %(message)s")

    main()