import socket as s
import time as t
import logging as l
import threading as th
import hashlib as h
import os

NOME_DO_SERVER = ''
PORTA_DO_SERVER = 6000
TAM_BUFFER = 2048
ENDERECO_IP = (NOME_DO_SERVER, PORTA_DO_SERVER)

# Funções padrão --------------------------------------------

def titulo():
    print("--------------------")
    print("      SERVIDOR")
    print("--------------------\n")


def print_mensagem(mensagem, mensagem_modificada, endereco_server):
    titulo()
    print("--------------------")
    print('Recebido: ', mensagem, ' - Enviou: ', mensagem_modificada, ' - Cliente: ', endereco_server)
    print("--------------------\n")


# def main():

logger = l.getLogger(__name__)
l.basicConfig(filename="server.log", encoding="utf-8", level=l.INFO, format="%(levelname)s - %(asctime)s: %(message)s")

inicializar = ''
iniciar_server = True
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
            erro_arquivo = ''

os.system('cls' if os.name == 'nt' else 'clear')
server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
server_socket.bind(ENDERECO_IP)
