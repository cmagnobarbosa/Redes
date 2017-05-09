#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
/*
Versão Inicial do servidor.
Com base no código: http://www.linuxhowtos.org/C_C++/socket.html
Obs: O servidor somente está rodando uma única vez.
*/

int main(){
	//Variaveis para estabelecer a comunicacao
	int socket_con = 0, new_socket_con = 0, num_porta = 5002, temp = 0;
	char mensagem[1024];
	char *resposta;
	socklen_t cliente_len;
	struct sockaddr_in endereco_servidor, endereco_cliente;

	// Abrindo o socket
	socket_con = socket(AF_INET, SOCK_STREAM,0); 
	if(socket_con < 0){
		printf("Erro ao criar o socket.\n");
	}

	//Preenche com zero.
	bzero((char *)&endereco_servidor, sizeof(endereco_servidor));
	endereco_servidor.sin_family = AF_INET;
	endereco_servidor.sin_addr.s_addr = INADDR_ANY;
	endereco_servidor.sin_port = htons(num_porta);

	if (bind(socket_con, (struct sockaddr *) &endereco_servidor,sizeof(endereco_servidor)) < 0){
		//Associa uma porta ao socket;
		printf("Erro ao Abrir a porta.\n");
	}

	//Tamanho maximo da fila de clientes.
	listen(socket_con, 5);

	//Estabelece a conexão com o cliente.
	new_socket_con = accept(socket_con,(struct sockaddr *) &endereco_cliente,&cliente_len);

	//Loop para troca de mensagens com o(s) cliente(s).
	while(new_socket_con >= 0){    
		cliente_len = sizeof(endereco_cliente);    
		if(new_socket_con < 0){
			printf("Erro ao conectar com o cliente.\n");
		}
		else
			printf("Conectado ao cliente: %d\n", new_socket_con);
		bzero(mensagem, 1024);

		//Realiza a leitura do socket.
		temp = read(new_socket_con, mensagem, 1024);
		if(temp < 0){
			printf("Erro ao ler o socket.\n");
		}
		printf("Mensagem %s", mensagem);

		//Escreve uma reposta no socket para o cliente. O último parametro é o numero de bytes.
		temp = write(new_socket_con,"Ok - Aguarde...", 15);
		if(temp < 0){
			printf("Erro ao escrever no socket\n");
		}		
	}

	//Fecha o socket de conexão com o cliente.
	close(new_socket_con); 
   
	//Fecha o socket que está ouvindo a porta.
	close(socket_con);


	return 0;
}
