/*
Versão Inicial do servidor.
Com base no código: http://www.linuxhowtos.org/C_C++/socket.html
*/
#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "cartas.h"

void embaralhar (){
	// As cartas estão ordenadas por ordem decrescente de valor
	// baralho[0].nome = "4p"; 	baralho[0].valor = 14;
	// baralho[1].nome = "7c"; baralho[1].valor = 13;
	// baralho[2].nome = "Ae"; baralho[2].valor = 12;
	// baralho[3].nome = "7o"; baralho[3].valor = 11;

	// baralho[4].nome = "3p"; baralho[4].valor = 10; 
	// baralho[5].nome = "3c"; baralho[5].valor = 10; 
	// baralho[6].nome = "3e"; baralho[6].valor = 10; 
	// baralho[7].nome = "3o"; baralho[7].valor = 10; 

	// baralho[8].nome = "2p"; baralho[8].valor = 9;
	// baralho[9].nome = "2c"; baralho[9].valor = 9;
	// baralho[10].nome = "2e"; baralho[10].valor = 9;
	// baralho[11].nome = "2o"; baralho[11].valor = 9;

	// baralho[12].nome = "Ap"; baralho[12].valor = 8;
	// baralho[13].nome = "Ac"; baralho[13].valor = 8;
	// baralho[14].nome = "Ao"; baralho[14].valor = 8;

	// baralho[15].nome = "Kp"; baralho[15].valor = 7;
	// baralho[16].nome = "Kc"; baralho[16].valor = 7;
	// baralho[17].nome = "Ke"; baralho[17].valor = 7;
	// baralho[18].nome = "Ko"; baralho[18].valor = 7;  

	// baralho[19].nome = "Jp"; baralho[19].valor = 6;
	// baralho[20].nome = "Jc"; baralho[20].valor = 6;
	// baralho[21].nome = "Je"; baralho[21].valor = 6;
	// baralho[22].nome = "Jo"; baralho[22].valor = 6;

	// baralho[23].nome = "Qp"; baralho[23].valor = 5;
	// baralho[24].nome = "Qc"; baralho[24].valor = 5;
	// baralho[25].nome = "Qe"; baralho[25].valor = 5;
	// baralho[26].nome = "Qo"; baralho[26].valor = 5;

	// baralho[27].nome = "7p"; baralho[27].valor = 4;
	// baralho[28].nome = "7e"; baralho[28].valor = 4;

	// baralho[29].nome = "6p"; baralho[29].valor = 3;
	// baralho[30].nome = "6c"; baralho[30].valor = 3;
	// baralho[31].nome = "6e"; baralho[31].valor = 3;
	// baralho[32].nome = "6o"; baralho[32].valor = 3;

	// baralho[33].nome = "5p"; baralho[33].valor = 2;
	// baralho[34].nome = "5c"; baralho[34].valor = 2;
	// baralho[35].nome = "5e"; baralho[35].valor = 2;
	// baralho[36].nome = "5o"; baralho[36].valor = 2;

	// baralho[37].nome = "4c"; baralho[37].valor = 1;
	// baralho[38].nome = "4e"; baralho[38].valor = 1;
	// baralho[39].nome = "4o"; baralho[39].valor = 1;
}

int main(){
	//Variaveis para estabelecer a comunicacao
	int socket_con = 0, num_porta = 5003, temp = 0;
	int cliente = 0, cliente2 = 0;
	char mensagem[1024];
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
		temp = write(cliente,"Ok - Aguarde...", 23);

		bzero(mensagem, 1024);
		
		//Realiza a leitura do socket do cliente 2.
		temp = read(cliente2, mensagem, 1024);
		printf("Mensagem do 2, %s\t e o temp vale: %d\n", mensagem,temp);

		//Escreve uma reposta no socket para o cliente. O último parametro é o numero de bytes.
		temp = write(cliente2,"Ok - Aguarde...", 23);
	}

	//Fecha o socket de conexão com o cliente.
	close(cliente); 
	close(cliente2);
   
	//Fecha o socket que está ouvindo a porta.
	close(socket_con);

	return 0;
}
