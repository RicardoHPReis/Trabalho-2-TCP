import socket as s
import time as t
import hashlib as h
import os

NOME_DO_SERVER = '127.0.0.1'
PORTA_DO_SERVER = 6000
TAM_BUFFER = 2048
ENDERECO_IP = (NOME_DO_SERVER, PORTA_DO_SERVER)

# Funções padrão --------------------------------------------

def titulo():
    print("--------------------")
    print("       CLIENTE")
    print("--------------------\n")


def opcoes():
    print('1) Solicitar arquivo.')
    print('2) Chat.')
    print('3) Conexão com o Servidor.\n')
    

def mensagem_envio(cliente_socket : s.socket, mensagem : str):
    cliente_socket.send(mensagem.encode())
    print("--------------------")
    print('Enviado: ', mensagem)
    print("--------------------\n")


def mensagem_recebimento(cliente_socket : s.socket):
    mensagem = cliente_socket.recv(TAM_BUFFER).decode('utf-8')
    print("--------------------")
    print('Recebido: ', mensagem)
    print("--------------------\n")
    return mensagem


def conectar_servidor():
    inicializar = ''
    iniciar_conexao = False
    while inicializar == '':
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        inicializar = input("Deseja conectar com o servidor [S/N] ? ").lower()
        match inicializar:
            case 's':
                iniciar_conexao = True
            case 'sim':
                iniciar_conexao = True
            case 'n':
                iniciar_conexao = False
            case 'não':
                iniciar_conexao = False
            case _:
                print('A escolha precisa estar nas opções acima!')
                t.sleep(2)
                inicializar = ''
    return iniciar_conexao
                

def escolher_arquivo(cliente_socket : s.socket):
    conjunto_arquivos = []
    num_arquivos = cliente_socket.recv(TAM_BUFFER).decode('utf-8')
    
    if int(num_arquivos) < 0 or not isinstance(num_arquivos, int):
        mensagem_envio(cliente_socket, 'ERROR-1-Má requisição')
    else:
        mensagem_envio(cliente_socket, 'OK-1-Confirmação')

    for i in range(0, int(num_arquivos)):
        recv_arquivo = mensagem_recebimento(cliente_socket)
        conjunto_arquivos.append(recv_arquivo)
        
    arquivo_disponivel = False
    while not arquivo_disponivel:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print('Arquivos disponíveis no servidor:')
        for arquivo in conjunto_arquivos:
            print(arquivo)

        nome_arquivo = input("\nDigite o nome do arquivo que você deseja receber: ")
        
        mensagem_envio(cliente_socket, nome_arquivo)
        
        ok_arq = mensagem_recebimento(cliente_socket)
        ok_arq = ok_arq.split("-")
    
        if(ok_arq[0] == 'OK'):
            arquivo_disponivel = True
        else:
            print('A escolha precisa estar nas opções acima!')
            t.sleep(2)


def receber_arquivo(cliente_socket : s.socket):
    print('Recebendo')
    

def requisitar_arquivo(cliente_socket : s.socket):
    escolher_arquivo(cliente_socket)
    receber_arquivo(cliente_socket)
    

def chat_servidor(cliente_socket : s.socket):
    print('Olá')


def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    cliente_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    cliente_socket.settimeout(30)

    iniciar_conexao = conectar_servidor()
    cliente_socket.connect(ENDERECO_IP)

    opcao = 0
    while iniciar_conexao:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        opcoes()
        opcao = int(input("Escolha uma opção: "))
        
        match opcao:
            case 1:
                requisitar_arquivo(cliente_socket)
            case 2:
                chat_servidor(cliente_socket)
            case 3:
                iniciar_conexao = conectar_servidor()
            case _:
                print('A escolha precisa estar nas opções acima!')
                t.sleep(2)
                print(opcao)
                print(type(opcao))
                opcao = 0
                
    cliente_socket.close()

if __name__ == "__main__":
    main()