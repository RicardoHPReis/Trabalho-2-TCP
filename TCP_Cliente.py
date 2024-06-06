import socket as s
import time as t
import logging as l
import hashlib as h
import threading as th
import os

NOME_DO_SERVER = '127.0.0.1'
PORTA_DO_SERVER = 6000
TAM_BUFFER = 2048
ENDERECO_IP = (NOME_DO_SERVER, PORTA_DO_SERVER)

logger = l.getLogger(__name__)
l.basicConfig(filename="cliente.log", encoding="utf-8", level=l.INFO, format="%(levelname)s - %(asctime)s: %(message)s")

# Funções padrão --------------------------------------------

def titulo():
    print("--------------------")
    print("       CLIENTE")
    print("--------------------\n")
    

def mensagem_envio(conexao_socket : s.socket, mensagem : str):
    try:
        conexao_socket.send(mensagem.encode())
        logger.info(f"Destinatário: {ENDERECO_IP} - Enviado:  '{mensagem}'")
    except:
        logger.info(f"Removido do Servidor:  {ENDERECO_IP}")
        conexao_socket.close()


def mensagem_recebimento(conexao_socket : s.socket):
    try:
        mensagem = conexao_socket.recv(TAM_BUFFER).decode('utf-8')
        logger.info(f"Remetente: {ENDERECO_IP} - Recebido: '{mensagem}'")
        return mensagem
    except:
        logger.info(f"Removido do Servidor:  {ENDERECO_IP}")
        conexao_socket.close()


def chat_envio(conexao_socket : s.socket, mensagem : str):
    try:
        conexao_socket.send(mensagem.encode())
        logger.info(f"Destinatário: {ENDERECO_IP} - Chat enviado:  '{mensagem}'")
    except:
        logger.info(f"Removido do Servidor:  {ENDERECO_IP}")
        conexao_socket.close()
    

def chat_recebimento(conexao_socket : s.socket):
    try:
        mensagem = conexao_socket.recv(TAM_BUFFER).decode('utf-8')
        logger.info(f"Remetente: {ENDERECO_IP} - Chat recebido: '{mensagem}'")
        return mensagem
    except:
        logger.info(f"Removido do Servidor:  {ENDERECO_IP}")
        conexao_socket.close()


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


def fechar_conexao(conexao_socket : s.socket):
    mensagem_envio(conexao_socket, 'OK-8-Desconectar servidor')
    resposta = mensagem_recebimento(conexao_socket).split("-")
    if resposta[0] == "OK":
        print("Conexão com servidor finalizado")
        t.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        return
    else:
        print("Erro ao fechar conexão")
        t.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
        return
               

def escolher_arquivo(conexao_socket : s.socket):
    conjunto_arquivos = []
    num_arquivos = int(mensagem_recebimento(conexao_socket))
    
    if not isinstance(num_arquivos, int):
        mensagem_envio(conexao_socket, 'ERROR-1-Má requisição')
    elif num_arquivos < 0:
        mensagem_envio(conexao_socket, 'ERROR-2-Tamanho incongruente')
    else:
        mensagem_envio(conexao_socket, 'OK-1-Confirmação')

    i = 0
    while i < num_arquivos:
        recv_arquivo = mensagem_recebimento(conexao_socket)
        mensagem_envio(conexao_socket, f"ACK-{i+1}")
        conjunto_arquivos.append(recv_arquivo)
        i+=1
        
        
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print('Arquivos disponíveis no servidor:')
        for arquivo in conjunto_arquivos:
            print(arquivo)

        nome_arquivo = input("\nDigite o nome do arquivo que você deseja receber: ")
        
        mensagem_envio(conexao_socket, nome_arquivo)
        
        ok_arq = mensagem_recebimento(conexao_socket).split("-")
    
        if(ok_arq[0] == 'OK'):
            break
        else:
            print('A escolha precisa estar nas opções acima!')
            t.sleep(2)
            
    return nome_arquivo


def requisitar_arquivo(conexao_socket : s.socket):
    nome_arquivo = escolher_arquivo(conexao_socket)
    
    pacotes = []
    name = nome_arquivo.split(".")
    nome_arquivo = name[0] + "_cliente." + name[1]
    dados = mensagem_recebimento(conexao_socket).split("-")
    
    if(dados[0] == "OK"):
        arquivo = open(nome_arquivo, "wb")
        num_pacotes = dados[2]
        num_digitos = dados[3]
        num_buffer = dados[4]
        checksum = dados[5]
        
        i = 0
        while i < num_pacotes:
            try:
                pack = conexao_socket.recv(TAM_BUFFER).decode('utf-8')
            except:
                logger.info(f"Removido do Servidor:  {ENDERECO_IP}")
                conexao_socket.close()
                
            pacote = descriptografar_arquivo(pack)
            pacote_valido = verificar_integridade_arquivo(pacote)
            if(pacote_valido):
                mensagem_envio(conexao_socket, f"ACK-{i+1}")
                arquivo.write(pack)
                i+=1
        
        arquivo.close()
        
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print('Arquivo Recebido com Sucesso')
        t.sleep(2)


def descriptografar_arquivo(pacote:bytes):
    print("Hash")
    return True

 
def verificar_integridade_arquivo(pacotes:bytes):
    print("Hash")
    return True


def chat_servidor(conexao_socket: s.socket):
    os.system('cls' if os.name == 'nt' else 'clear')
    titulo()
    print("CHAT SERVIDOR X CLIENTE\n\n")
    cliente_msg = ""
    servidor_msg = ""
    
    while servidor_msg.lower() != "sair":
        cliente_msg = input(f"<{ENDERECO_IP}> ")
        chat_envio(conexao_socket, cliente_msg[:1024])
        if cliente_msg.lower() == "sair":
            break

        servidor_msg = chat_recebimento(conexao_socket)
        print(f"<Servidor> {servidor_msg}")
        

def opcoes_cliente(conexao_socket : s.socket):
    os.system('cls' if os.name == 'nt' else 'clear')
    titulo()
    print('1) Solicitar arquivo.')
    print('2) Chat.')
    print('3) Fechar conexão com o Servidor.\n')
    
    opcao = int(input("Escolha uma opção: "))
    match opcao:
        case 1:
            mensagem_envio(conexao_socket, 'OPTION-1-Requisição de arquivo')
            requisitar_arquivo(conexao_socket)
            opcoes_cliente(conexao_socket)
        case 2:
            mensagem_envio(conexao_socket, 'OPTION-2-Chat')
            chat_servidor(conexao_socket)
            opcoes_cliente(conexao_socket)
        case 3:
            mensagem_envio(conexao_socket, 'OPTION-3-Desconectando do Servidor')
            fechar_conexao(conexao_socket)
        case _:
            print('A escolha precisa estar nas opções acima!')
            t.sleep(2)
            opcoes_cliente(conexao_socket)
            
            
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    conexao_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    conexao_socket.settimeout(30)

    iniciar_conexao = conectar_servidor()
    conexao_socket.connect(ENDERECO_IP)

    try:
        if iniciar_conexao:
            opcoes_cliente(conexao_socket)
    except TimeoutError:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print("ERROR-5-Excedeu-se o tempo para comunicação entre o servidor e o cliente!")
    except Exception as e:
        os.system('cls' if os.name == 'nt' else 'clear')
        titulo()
        print("ERROR-0-Erro não registrado!")
        print(e)


if __name__ == "__main__": 
    main()