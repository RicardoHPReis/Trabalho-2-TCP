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
    print("--------------------")
    print('Enviado: ', mensagem)
    print("--------------------\n")


def mensagem_recebimento(servidor_socket : s.socket):
    mensagem = servidor_socket.recv(TAM_BUFFER).decode('utf-8')
    print("--------------------")
    print('Recebido: ', mensagem)
    print("--------------------\n")
    return mensagem
    

def iniciar_servidor():
    inicializar = ''
    iniciar_server = False
    while inicializar == '':
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        inicializar = input("Deseja inicializar o servidor [S/N] ? ").lower()
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


def retornar_nome_arquivos(conexao_socket:s.socket):
    os.system('cls' if os.name == 'nt' else 'clear')

    caminho = str(p.Path.cwd()) + '\Arquivos'
    file_paths = os.listdir(caminho)
    num_arquivos = len(file_paths)

    conexao_socket.send(str(num_arquivos).encode())
    
    confirmacao_tam = conexao_socket.recv(TAM_BUFFER)
    
    if(confirmacao_tam != b'Recebido'):
        conexao_socket.send("ERROR-1-Tamanho não recebido".encode())
        return
    
    for i in range(0, num_arquivos):
        conexao_socket.send(file_paths[i].encode())
    
    nome_arquivo = conexao_socket.recv(TAM_BUFFER).decode('utf-8')
    
    if not os.path.exists(os.path.join("./Arquivos", nome_arquivo)):
        conexao_socket.send("ERROR-1-Arquivo não encontrado!".encode())
        return
    
    
def enviar_arquivo(conexao_socket:s.socket):
    os.system('cls' if os.name == 'nt' else 'clear')

    caminho = str(p.Path.cwd()) + '\Arquivos'
    file_paths = os.listdir(caminho)
    num_arquivos = len(file_paths)

    conexao_socket.send(str(num_arquivos).encode())
    ok_tam = conexao_socket.recv(TAM_BUFFER).decode('utf-8')
    ok_tam = ok_tam.split("-")
    
    if(ok_tam[0] != 'OK'):
        conexao_socket.send("ERROR-1-Tamanho não recebido".encode())
        return
    else:
        for i in range(0, num_arquivos):
            conexao_socket.send(file_paths[i].encode())
        
        nome_arquivo = conexao_socket.recv(TAM_BUFFER).decode('utf-8')
        
        if not os.path.exists(os.path.join("./Arquivos", nome_arquivo)):
            conexao_socket.send("ERROR-1-Arquivo não encontrado!".encode())
            return


def main():
    logger = l.getLogger(__name__)
    l.basicConfig(filename="server.log", encoding="utf-8", level=l.INFO, format="%(levelname)s - %(asctime)s: %(message)s")

    os.system('cls' if os.name == 'nt' else 'clear')
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    server_socket.bind(ENDERECO_IP)
    server_socket.listen()
    server_socket.settimeout(30)

    iniciar_server = iniciar_servidor()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Esperando resposta')

    while iniciar_server:
        conexao_socket, endereco = server_socket.accept()
        retornar_nome_arquivos(conexao_socket)
        #thread = th.Thread(target=retornar_nome_arquivos, args=(conexao_socket), daemon=True)
        #thread.start()
        conexao_socket.close()
        

if __name__ == "__main__":
    main()