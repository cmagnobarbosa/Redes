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
*/

int main(){
	//Variaveis para estabelecer a comunicacao
	int socket_con = 0, num_porta = 5003, temp = 0;
	int cliente = 0, cliente2 = 0;
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

	//Estabelece a conexão com os clientes.
	cliente = accept(socket_con,(struct sockaddr *) &endereco_cliente, &cliente_len);
	cliente2 = accept(socket_con,(struct sockaddr *) &endereco_cliente, &cliente_len);

	if(cliente < 0 || cliente2 < 0){
			printf("Erro ao conectar com o cliente.\n");
		}
		else
			printf("Conectado aos clientes: %d e %d\n", cliente, cliente2);

	//Loop para troca de mensagens com o(s) cliente(s).
	for(;;){    
		cliente_len = sizeof(endereco_cliente);		
		bzero(mensagem, 1024);

		//Realiza a leitura do socket do cliente 1.
		temp = read(cliente, mensagem, 1024);
		printf("Mensagem %s\t e o temp vale: %d\n", mensagem,temp);

		//Escreve uma reposta no socket para o cliente. O último parametro é o numero de bytes.
		temp = write(cliente,"Ok - Aguarde...", 15);

		bzero(mensagem, 1024);
		
		//Realiza a leitura do socket do cliente 2.
		temp = read(cliente2, mensagem, 1024);
		printf("Mensagem do 2, %s\t e o temp vale: %d\n", mensagem,temp);

		//Escreve uma reposta no socket para o cliente. O último parametro é o numero de bytes.
		temp = write(cliente2,"Ok - Aguarde...", 15);	
	}

	//Fecha o socket de conexão com o cliente.
	close(cliente); 
   
	//Fecha o socket que está ouvindo a porta.
	close(socket_con);

	return 0;
}
