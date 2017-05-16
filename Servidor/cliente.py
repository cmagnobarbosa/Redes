import socket

# Dados do cliente para conexao como server
ipServidor = 'localhost'
portaServidor = 5001


# Cria o objeto socket e conecta ao servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Definicao do servidor como TCP IP



cliente.connect((ipServidor, portaServidor))

#cliente.send('lucas')

# Resposta do servidor
data = cliente.recv(1024)

print data

s = raw_input("Digete:")
cliente.send(s)



