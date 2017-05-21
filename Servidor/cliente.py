# coding: utf-8
import socket


def traduzCarta():
	pass

def traduzPlacar():
	pass

def pedirTruco(mensagem):
	mensagem_aux = ''

	mensagem_aux += mensagem[:19]
	mensagem_aux += "1"
	mensagem_aux += mensagem[20:]

	print "\n\tAguardando resposta do oponente..."

	return mensagem_aux

def respTruco(mensagem, op):
	mensagem_aux = ''

	mensagem_aux += mensagem[:21]
	if(op == "1"):
		mensagem_aux += "1" # Aceitar truco
	elif(op == "2"):
		mensagem_aux += "0"	# Correr do truco
	mensagem_aux += mensagem[22:]

	return mensagem_aux
	

def jogarCarta(mensagem, cliente_mao, op, cliente_Id):
	"""
	Realiza alteração na mensagem, inserindo no campo 'mesa' a carta jogada pelo cliente
	"""
	mensagem_aux = ''

	if(cliente_Id == '0'):
		mensagem_aux += mensagem[:22]
		mensagem_aux += cliente_mao[op]
		mensagem_aux += mensagem[24:]
		cliente_mao.pop(op)

	if(cliente_Id == '1'):
		mensagem_aux += mensagem[:24]
		mensagem_aux += cliente_mao[op]
		mensagem_aux += mensagem[26:]
		cliente_mao.pop(op)

	if(cliente_Id == '2'):
		mensagem_aux += mensagem[:26]
		mensagem_aux += cliente_mao[op]
		mensagem_aux += mensagem[28:]
		cliente_mao.pop(op)
	
	if(cliente_Id == '3'):
		mensagem_aux += mensagem[:28]
		mensagem_aux += cliente_mao[op]
		mensagem_aux += mensagem[30:]
		cliente_mao.pop(op)

	return mensagem_aux

def acao(mensagem, cliente_Id, cliente_Eq, cliente_mao):
	print "\nSua vez:"
	opcoes = []
	cont = 0
	op = ''
	l = ['1', '2']
	valor = int(mensagem[17:19])
	placarA = mensagem[10:12]
	placarB = mensagem[12:14]

	# Caso o adversario tenha pedido truco
	if(mensagem[19:20] == "1"):
		if(mensagem[17:19] == "01"):
			print "\n\t Seu adversario pediu truco..."
		else:
			print "\n\t Seu adversario pediu", valor + 3
		
		print "Escolha:"
		while(op not in l):
			print "1 - Aceitar"
			print "2 - Correr"
			op = raw_input("Opçao: ")
			if(op not in l):
				print "\nOpção inválida!\nEscolha:"

		mensagem = respTruco(mensagem, op)
		return mensagem


	# Caso haja a possibilidade de pedir truco	
	elif(valor < 12 and 
		(mensagem[20:21] == "0" or mensagem[20:21] == cliente_Eq) and
		 (placarA is not "12" and placarB is not "12")):		

		# Caso o usuario digite uma opção invalida
		while(op not in l): 
			print "1 - Jogar Carta"
			if(mensagem[17:19] == "01"):
				print "2 - Pedir truco"
			else:
				print "2 - Pedir %d" % (int(mensagem[17:19]) + 3)
			op = raw_input("Opçao: ")
			if(op not in l):
				print "\nOpção inválida!\nSua vez:"
	else:
		op = "1"

	# Jogar carta	
	if(op is "1"):
		while(op not in opcoes):
			print "\nEscolha uma carta para jogar:"
			opcoes = []
			cont = 0
			for i in cliente_mao:
				print cont, "-", i
				opcoes.append(cont)
				cont += 1
				
			op = raw_input("Opçao: ")
			try:
				op = int(op)
				if(op not in opcoes):
					print "\nOpção invalida! Digite uma das opções disponiveis"
			except Exception:
				print "\nOpção invalida! Digite uma das opções disponiveis"		
			
		
		mensagem = jogarCarta(mensagem, cliente_mao, op, cliente_Id)
		return mensagem

	# Pedir truco
	elif(op is "2"):
		mensagem = pedirTruco(mensagem)
		return mensagem



def info(mensagem):
	"""
	Informa ao cliente a situação do jogo, sempre que algum outro jogador
	realiza alguma ação
	"""

	print "******************* Info **********************"

	print ("Mesa\nid 0: %s | id 1: %s | id 2: %s | id 3: %s" 
		   % (mensagem[22:24], mensagem[24:26], mensagem[26:28], mensagem[28:30]))
	
	print ("\nPlacar da Rodada:[%s] [%s] [%s]"
		   % (mensagem[14:15], mensagem[15:16], mensagem[16:17]))

	print ("\nValor da Rodada: " + mensagem[17:19])

	print ("\nPlacar do jogo\nA: %s \t B: %s"
		   % (mensagem[10:12], mensagem[12:14]))

	print "***********************************************\n"

def takeCards(cartas):
	"""
	Retorna a lista de strngs 'mao' com as cartas recebidas pelo jogador apos uma nova distribuição
	"""

	mao = []
	mao.append(cartas[0:2])
	mao.append(cartas[2:4])
	mao.append(cartas[4:6])
	return mao


def main():
	# Dados do cliente para conexao como server
	ipServidor = ''
	portaServidor = 5001

	# Variaveis 
	cliente_mao = []
	cliente_Id = ''
	cliente_Eq = ''
	mensagem = ''

	# Cria o objeto socket e conecta ao servidor
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Definicao do servidor como TCP IP

	try:
		cliente.connect((ipServidor, portaServidor)) # Estabelecendo conexão com o servidor
		print "Cliete conectado ao servidor!"

	except Exception:
		print "Erro ao conectar ao servidor!"
		return None

	print "\n--------------- Inicio do jogo ----------------\n"
	mensagem = cliente.recv(31)
	cliente_Id = mensagem[:1]
	cliente_Eq = mensagem [1:2]
	cliente_mao = takeCards(mensagem[4:10])

	if(cliente_Id is "0"):
		print "Seu Id é 0\nsua equipe é 'a' -> Ids(0 e 2)\n"
	elif(cliente_Id is "1"):
		print "Seu Id é 1\nsua equipe é 'b' -> Ids(1 e 3)"
	elif(cliente_Id is "2"):
		print "Seu Id é 2\nsua equipe é 'a' -> Ids(0 e 2)"	
	elif(cliente_Id is "3"):
		print "Seu Id é 3\nsua equipe é 'b' -> Ids(1 e 3)"	
	print "Nova rodada! Sua mão é: ", mensagem[4:10]

	while True:
		mensagem = cliente.recv(31)
		placarA = int(mensagem[10:12])
		placarB = int(mensagem[12:14])

		# Se o jogo ja tiver um vencedor
		if(placarA >= 12 or placarB >= 12):
			break;

		# O servidor enviou uma nova mao para o cliente
		if(mensagem[4:5] is not "0"): 
			cliente_mao = takeCards(mensagem[4:10])
			print "\nNova rodada! Sua mão é: ", mensagem[4:10], "\n"
			info(mensagem)

		else:
			if(mensagem[2:3] is "1"): # Vez do cliente
				print "\n\txxxxxxx " + mensagem
				mensagem = acao(mensagem, cliente_Id, cliente_Eq, cliente_mao)
				print "mensagem para envio " , mensagem
				cliente.send(mensagem)
				
			elif(mensagem[2:3] is "0" and mensagem[19:20] is not "1"):
				info(mensagem) 	


	if(int(mensagem[10:12]) >= 12):
		print "\n\n\tFim de jogo! Equipe A venceu o jogo!"

	if(int(mensagem[12:14]) >= 12):	
		print "\n\n\tFim de jogo! Equipe B venceu o jogo!"


		cliente.close()

if __name__ == '__main__':
	main()



