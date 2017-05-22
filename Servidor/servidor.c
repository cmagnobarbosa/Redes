/*
Desenvolvido por:
	- Carlos Magno Geraldo Barbosa
	- Lucas Geraldo Silva Cruz

Licença: MIT
Disciplina: Redes de Computadores
Universidade Federal de São João del Rei - UFSJ
*/

#include <strings.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include "truco.h"

int main(){
	/* Variaveis para estabelecer a comunicacao */
	int socket_con = 0, num_porta = 5000, temp = 0;
	socklen_t cliente_len;
	struct sockaddr_in endereco_servidor, endereco_cliente;

	/* Variaveis do jogo */
	int i, j, saida = 0, volta, vencedor, flag = 0, aux = 0 ;
	char mensagem[32], token[9], strAux[9];
	char vez[2], rodada[2], placarJogo[5], placarRodada[4], valorRodada[3];
	char question[2], eqQuestion[2], respQuestion[2], mesa[9];
	carta baralho[40];
	jogador clientes[4];

	/* Abrindo o socket */
	socket_con = socket(AF_INET, SOCK_STREAM,0); 
	if(socket_con < 0)
		printf("Erro ao criar o socket.\n");

	/* Preenche com zero */
	bzero((char *)&endereco_servidor, sizeof(endereco_servidor));
	endereco_servidor.sin_family = AF_INET;
	endereco_servidor.sin_addr.s_addr = INADDR_ANY;
	endereco_servidor.sin_port = htons(num_porta);

	/* Associa uma porta ao socket */
	if (bind(socket_con, (struct sockaddr *) &endereco_servidor,sizeof(endereco_servidor)) < 0)
		printf("Erro ao Abrir a porta.\n");
	else
		printf("Aguardando conexão dos 4 clientes...\n");	

	/* Tamanho maximo da fila de clientes. */
	listen(socket_con, 5);
	
	/* Estabelece a conexão com os clientes */
	for(i = 0; i < 4; i++){
		clientes[i].porta = accept(socket_con,(struct sockaddr *) &endereco_cliente, &cliente_len); // Atribuindo a porta
		bzero(strAux,9);	
		strAux[0] = i + 48;
		strcpy(clientes[i].id, strAux); // Atribuindo id

		if(i % 2 == 0)
			strcpy(clientes[i].equipe, "a"); // Atribuindo a equipe A
		else
			strcpy(clientes[i].equipe, "b"); // Atribuindo a equipe B
	}

	if(clientes[0].porta < 0 || clientes[1].porta < 0 || 
	   clientes[2].porta < 0 || clientes[3].porta < 0)
	   printf("Erro ao conectar com o cliente.\n");
	else{
		for(i = 0; i < 4; i++)
			printf("Conectado ao cliente: %s porta %d\n", clientes[i].id, clientes[i].porta);
	}		

	cliente_len = sizeof(endereco_cliente);

	/* Loop para troca de mensagens com os clientes */
	strcpy(placarJogo, "0000");
	for(;;){
		embaralhar(baralho);
		distribuir(baralho, clientes);

		bzero(mensagem, 32); //Zera o buffer de mensagens
		strcpy(mensagem, "000000000000000000000000000000\n"); // Mensagem inicial
		setToken(mensagem, 10, 13, placarJogo);

		entregar(clientes, mensagem);
		sleep(1);

		flag = 0;
		volta = saida;
		if(maoDe11(placarJogo)) // Se estiver na mao de 11 a rodada vale 3
			strcpy(valorRodada, "03");
		else
			strcpy(valorRodada, "01");

		strcpy(eqQuestion,"0");

		for(i = 0; i < 3; i++){    // Rodada: 3 turnos
			rodada[0] = i + 49;
			strcpy(mesa, "00000000");
			strcpy(placarRodada, getToken(mensagem, 14, 16, placarRodada));

			for(j = 0; j < 4; j++){   // Turno: 4 jogadores->(4 jogadas)
				printf("Vez do jogador id: %d\n", volta);
				unirMsg(mensagem, "1", rodada, placarJogo, placarRodada,
			 			valorRodada, "0", eqQuestion,
			 			"0", mesa, "E");
				write(clientes[volta].porta, mensagem, 31);
				read(clientes[volta].porta, mensagem, 31);
				broadCast(mensagem, clientes);

				// Caso tenha um pedido truco, seis, etc
				if(strcmp(getToken(mensagem, 17, 18, strAux), "12") != 0 && mensagem[19] == '1'){ 
					aux = volta;
					printf("\nJogador %d pediu truco. \n", volta);

					if(aux == 3){						
						setToken(mensagem, 20, 20, clientes[0].equipe);
						strcpy(eqQuestion, clientes[0].equipe);
						broadCast(mensagem, clientes);
						sleep(1);

						setToken(mensagem, 2, 2, "1"); 
						printf("Vez do jogador 0.\n");
						write(clientes[0].porta, mensagem, 31);
						read(clientes[0].porta, mensagem, 31);

						if(mensagem[21] == '1'){
							printf("\nJogador 0 aceitou o truco! \n");
							truco(mensagem, valorRodada);
							setToken(mensagem, 19, 19, "0"); // zerando question
							setToken(mensagem, 21, 21, "0"); // zerando rep_question
							broadCast(mensagem, clientes);
							sleep(1);

							setToken(mensagem, 2, 2, "1"); 
							printf("Vez do jogador 3\n");
							write(clientes[3].porta, mensagem, 31);
							read(clientes[3].porta, mensagem, 31);
							broadCast(mensagem, clientes);
						}
						else{
							setToken(mensagem, 19, 19, "0"); // zerando question
							setToken(mensagem, 21, 21, "0"); // zerando rep_question
							printf("\nJogador 0 correu.\n");
							sleep(1);
							flag = 1;
							break;
						}			
					}
					else{
						setToken(mensagem, 20, 20, clientes[aux+1].equipe);
						strcpy(eqQuestion, clientes[aux+1].equipe);
						broadCast(mensagem, clientes);
						sleep(1);

						setToken(mensagem, 2, 2, "1"); 
						printf("Vez do jogador %d\n", volta + 1);
						write(clientes[aux+1].porta, mensagem, 31);
						read(clientes[aux+1].porta, mensagem, 31);

						if(mensagem[21] == '1'){
							printf("\nJogador %d aceitou o truco.\n", volta + 1);
							truco(mensagem, valorRodada);
							setToken(mensagem, 19, 19, "0"); // zerando question
							setToken(mensagem, 21, 21, "0"); // zerando rep_question
							broadCast(mensagem, clientes);
							sleep(1);

							setToken(mensagem, 2, 2, "1"); 
							printf("Vez do jogador %d\n", volta);
							write(clientes[aux].porta, mensagem, 31);
							read(clientes[aux].porta, mensagem, 31);
							broadCast(mensagem, clientes);
						}
						else if(mensagem[21] == '0'){
							setToken(mensagem, 19, 19, "0"); // zerando question
							setToken(mensagem, 21, 21, "0"); // zerando rep_question
							printf("\nJogador %d correu. \n", volta + 1);
							sleep(1);
							flag = 1;
							break;
						}
					}
				}
				
				strcpy(mesa, getToken(mensagem, 22, 29, mesa));

				if(volta == 3)
					volta = 0;
				else{
					volta++;
				}

			}

			if(flag == 1){    // Caso a equipe tenha corrido do truco
				flag = 0;
				printf("\nA equipe  '%s'  venceu a rodada!\n\n", clientes[volta].equipe );
				mudaPlacar(placarJogo, valorRodada, clientes[volta].equipe);	
				setToken(mensagem, 10, 13, placarJogo);
				broadCast(mensagem, clientes);
				sleep(1);
				break;
			}
			vencedor = vencTurno(mensagem, baralho); // Retorna jogador que venceu o turno
			setToken(mensagem, 22, 29, "00000000"); // limpando mesa

			if(vencedor >= 10){
				setToken(mensagem, 14+i, 14+i, "-");
				printf("\nEmpate no turno %d \n", i+1);
				volta = vencedor-10; 		// jogador que empatou volta
			}
			else if(vencedor % 2 == 0){
				setToken(mensagem, 14+i, 14+i, "a");
				printf("\nJogador %d da equipe A venceu o %d turno!\n", vencedor, i+1);
				volta = vencedor;
			}
			else{
				setToken(mensagem, 14+i, 14+i, "b");
				printf("\nJogador %d da equipe B venceu o %d turno!\n", vencedor, i+1);
				volta = vencedor;
			}
			broadCast(mensagem, clientes);

			if(vencRodada(mensagem, placarJogo)){ // Se alguma equipe houver vencido a rodada	
				setToken(mensagem, 10, 13, placarJogo);
				broadCast(mensagem, clientes);
				sleep(2);
				break;			
			}

		}
		
		if(saida == 3)
			saida = 0 ;
		else
			saida++;

		if(vencJogo(mensagem)){
			broadCast(mensagem, clientes);
			break;
		}

	}

	/* Fecha o socket de conexão com o cliente */
	for(i = 0; i < 4; i++)
		close(clientes[i].porta);

	/* Fecha o socket que está ouvindo a porta */
	close(socket_con);
	return 0;
}

