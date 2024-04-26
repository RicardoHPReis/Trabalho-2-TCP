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


def print_envio(mensagem):
    print("--------------------")
    print('Enviado: ', mensagem)
    print("--------------------\n")


def print_recebimento(mensagem_modificada, endereco_server):
    print("--------------------")
    print('Recebido: ', mensagem_modificada, ' - Servidor: ', endereco_server)
    print("--------------------\n")

# def main():

cliente_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
cliente_socket.settimeout(60)