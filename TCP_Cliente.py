import socket as s
import time as t
import hashlib as h
import threading as th
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
    num_arquivos = int(num_arquivos)
    
    if not isinstance(num_arquivos, int):
        mensagem_envio(cliente_socket, 'ERROR-1-Má requisição')
    elif num_arquivos < 0:
        mensagem_envio(cliente_socket, 'ERROR-2-Tamanho incongruente')
    else:
        mensagem_envio(cliente_socket, 'OK-1-Confirmação')

    for i in range(0, int(num_arquivos)):
        recv_arquivo = mensagem_recebimento(cliente_socket)
        conjunto_arquivos.append(recv_arquivo)
        
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print('Arquivos disponíveis no servidor:')
        for arquivo in conjunto_arquivos:
            print(arquivo)

        nome_arquivo = input("\nDigite o nome do arquivo que você deseja receber: ")
        
        mensagem_envio(cliente_socket, nome_arquivo)
        
        ok_arq = mensagem_recebimento(cliente_socket).split("-")
    
        if(ok_arq[0] == 'OK'):
            break
        else:
            print('A escolha precisa estar nas opções acima!')
            t.sleep(2)


def requisitar_arquivo(cliente_socket : s.socket):
    escolher_arquivo(cliente_socket)
    print('Recebendo')
    

def receber_mensagem_servidor(cliente : s.socket):
  while True:
      try:
          msg = cliente.recv(TAM_BUFFER).decode('utf-8').strip()
          print(msg)
          if(msg == "Sair"):
                break
      except:
          return


def enviar_mensagem_servidor(cliente : s.socket, username):
  while True:
      try:
          msg = input()
          cliente.send(f'<{username}> {msg}'.encode('utf-8'))
      except:
          return

def chat_servidor(client : s.socket, username : str):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Chat CLIENTE X SERVIDOR")
    while True:
        thread_receber_msg = th.Thread(target=receber_mensagem_servidor, args=[client])
        thread_enviar_msg = th.Thread(target=enviar_mensagem_servidor, args=[client, username])

        thread_receber_msg.start()
        thread_enviar_msg.start()
        

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    cliente_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    cliente_socket.settimeout(30)

    iniciar_conexao = conectar_servidor()
    username = input("Digite o nome do usuário: ").strip()
    cliente_socket.connect(ENDERECO_IP)

    opcao = 0
    try:
        while iniciar_conexao:
            os.system('cls' if os.name == 'nt' else 'clear')
            titulo()
            opcoes()
            opcao = int(input("Escolha uma opção: "))
            match opcao:
                case 1:
                    mensagem_envio(cliente_socket, 'OPTION-1-Requisição de arquivo')
                    requisitar_arquivo(cliente_socket)
                case 2:
                    mensagem_envio(cliente_socket, 'OPTION-2-Chat')
                    chat_servidor(cliente_socket, username)
                case 3:
                    iniciar_conexao = conectar_servidor()
                    if not iniciar_conexao:
                        mensagem_envio(cliente_socket, 'OPTION-3-Desconectar servidor')
                case _:
                    print('A escolha precisa estar nas opções acima!')
                    t.sleep(2)
                    opcao = 0
                    
    except TimeoutError:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print("ERROR-5-Excedeu-se o tempo para comunicação entre o servidor e o cliente!")
        
    except Exception as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print("ERROR-0-Erro não registrado!")
        print(e)
                
    cliente_socket.close()

if __name__ == "__main__":
    main()