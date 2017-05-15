/*
Versão Inicial do servidor.
Com base no código: http://www.linuxhowtos.org/C_C++/socket.html

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
#include "header.h"

void embaralhar(carta baralho[40]);

void distribuir(carta baralho[40], jogador clientes[4]);

void entregar(jogador clientes[4], char mensagem[32]);

int getValor(char *nome, carta baralho[40]);

char* getToken(char mensagem[32], int inicio, int fim, char *token);

void setToken(char mensagem[32], int inicio, int fim, char *token);

int vencTurno(char mensagem[32], carta baralho[40]);

int vencRodada(char mensagem[32], char *placarJogo);

int vencJogo(char mensagem [32]);

int maoDe11(char *placarJogo);

void unirMsg(char mensagem[32], char *vez, char *rodada, char *placarJogo, char *placarRodada,
			 char *valorRodada, char *question, char *eqQuestion,
			 char *respQuestion, char *mesa, char *virada);

void broadCast(char mensagem[32], jogador clientes[4]);

int main(){
	/* Variaveis para estabelecer a comunicacao */
	int socket_con = 0, num_porta = 5001, temp = 0;
	socklen_t cliente_len;
	struct sockaddr_in endereco_servidor, endereco_cliente;

	/* Variaveis do jogo */
	int i, j, saida = 0, volta, vencedor;
	char mensagem[32], token[9], strAux[9];
	char vez[2], rodada[2], placarJogo[5], placarRodada[4], valorRodada[3];
	char question[2], eqQuestion[2], respQuestion[2], mesa[9], virada[2];
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
		printf("Aguardando conexão dos clientes...\n");

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

	cliente_len = sizeof(endereco_cliente);	//???




	/*  Realiza a leitura do socket do cliente
		temp = read(clientes[0].porta, mensagem, 23);
		printf("Mensagem: %s   e o temp vale: %d\n", mensagem,temp);

		Escreve uma reposta no socket para o cliente.
		O último parametro é o numero de bytes */

	/* Loop para troca de mensagens com os clientes */
	strcpy(placarJogo, "0000");
	for(;;){
		embaralhar(baralho);
		distribuir(baralho, clientes);

		bzero(mensagem, 32); //Zera o buffer de mensagens
		strcpy(mensagem, "000000000000000000000000000000\n"); // Mensagem inicial
		entregar(clientes, mensagem);

		volta = saida;
		if(maoDe11(placarJogo))
			strcpy(valorRodada, "12");
		else
			strcpy(valorRodada, "12");

		for(i = 0; i < 3; i++){    // Rodada: 3 turnos
			rodada[0] = i + 49;
			strcpy(mesa, "00000000");
			strcpy(placarRodada, getToken(mensagem, 14, 16, placarRodada));
			//strcpy(placarJogo, getToken(mensagem, 10, 13, placarJogo));

			for(j = 0; j < 4; j++){   // Turno: 4 jogadores->(4 jogadas)
				printf("Vez do jogador id: %d\n", volta);
				unirMsg(mensagem, "1", rodada, placarJogo, placarRodada,
			 			valorRodada, "0", "0",
			 			"0", mesa, "E");

				sleep(1);
				write(clientes[volta].porta, mensagem, 31);
				read(clientes[volta].porta, mensagem, 31);
				broadCast(mensagem, clientes);

				strcpy(mesa, getToken(mensagem, 22, 29, mesa));

				if(volta == 3)
					volta = 0;
				else
					volta++;
			}

			vencedor = vencTurno(mensagem, baralho);
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

			if(vencRodada(mensagem, placarJogo)){
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
			break;
		}

		// write(clientes[0].porta, "1a004p7c7o000000000000000000000", 32);
		// write(clientes[1].porta, "1a004p7c7o000000000000000000000", 32);

		/*unirMsg(mensagem, vez, rodada, placarJogo, placarRodada,
			 			valorRodada, question, eqQuestion,
			 			respQuestion, mesa, virada); */

		//read(clientes[volta].porta, mensagem, 23);
	}

	/* Fecha o socket de conexão com o cliente */
	for(i = 0; i < 4; i++)
		close(clientes[i].porta);

	/* Fecha o socket que está ouvindo a porta */
	close(socket_con);
	return 0;
}

void embaralhar(carta baralho[40]){
/* Esta função atribui os nomes e valores de cada carta
   do baralho de truco a uma poisição do array baralho */
	// As cartas estão ordenadas por ordem decrescente de valor
	strcpy(baralho[0].nome , "4p"); baralho[0].valor = 14;
	strcpy(baralho[1].nome , "7c"); baralho[1].valor = 13;
	strcpy(baralho[2].nome , "ae"); baralho[2].valor = 12;
	strcpy(baralho[3].nome , "7o"); baralho[3].valor = 11;

	strcpy(baralho[4].nome , "3p"); baralho[4].valor = 10;
	strcpy(baralho[5].nome , "3c"); baralho[5].valor = 10;
	strcpy(baralho[6].nome , "3e"); baralho[6].valor = 10;
	strcpy(baralho[7].nome , "3o"); baralho[7].valor = 10;

	strcpy(baralho[8].nome , "2p"); baralho[8].valor = 9;
	strcpy(baralho[9].nome , "2c"); baralho[9].valor = 9;
	strcpy(baralho[10].nome, "2e"); baralho[10].valor = 9;
	strcpy(baralho[11].nome, "2o"); baralho[11].valor = 9;

	strcpy(baralho[12].nome, "ap"); baralho[12].valor = 8;
	strcpy(baralho[13].nome, "ac"); baralho[13].valor = 8;
	strcpy(baralho[14].nome, "ao"); baralho[14].valor = 8;

	strcpy(baralho[15].nome, "kp"); baralho[15].valor = 7;
	strcpy(baralho[16].nome, "kc"); baralho[16].valor = 7;
	strcpy(baralho[17].nome, "ke"); baralho[17].valor = 7;
	strcpy(baralho[18].nome, "ko"); baralho[18].valor = 7;

	strcpy(baralho[19].nome, "jp"); baralho[19].valor = 6;
	strcpy(baralho[20].nome, "jc"); baralho[20].valor = 6;
	strcpy(baralho[21].nome, "je"); baralho[21].valor = 6;
	strcpy(baralho[22].nome, "jo"); baralho[22].valor = 6;

	strcpy(baralho[23].nome, "qp"); baralho[23].valor = 5;
	strcpy(baralho[24].nome, "qc"); baralho[24].valor = 5;
	strcpy(baralho[25].nome, "qe"); baralho[25].valor = 5;
	strcpy(baralho[26].nome, "qo"); baralho[26].valor = 5;

	strcpy(baralho[27].nome, "7p"); baralho[27].valor = 4;
	strcpy(baralho[28].nome, "7e"); baralho[28].valor = 4;

	strcpy(baralho[29].nome, "6p"); baralho[29].valor = 3;
	strcpy(baralho[30].nome, "6c"); baralho[30].valor = 3;
	strcpy(baralho[31].nome, "6e"); baralho[31].valor = 3;
	strcpy(baralho[32].nome, "6o"); baralho[32].valor = 3;

	strcpy(baralho[33].nome, "5p"); baralho[33].valor = 2;
	strcpy(baralho[34].nome, "5c"); baralho[34].valor = 2;
	strcpy(baralho[35].nome, "5e"); baralho[35].valor = 2;
	strcpy(baralho[36].nome, "5o"); baralho[36].valor = 2;

	strcpy(baralho[37].nome, "4c"); baralho[37].valor = 1;
	strcpy(baralho[38].nome, "4e"); baralho[38].valor = 1;
	strcpy(baralho[39].nome, "4o"); baralho[39].valor = 1;
}

void distribuir(carta baralho[40], jogador clientes[4]){
/* Esta função distribui as cartas aleatoriamenteentre os jogadores */
	int i,j,k = 0;
	int card[12];
    srand(time(NULL));

	for(i = 0; i < 12; i++){
        card[i] = rand()%40;
        for(j = 0; j < i; j++){
            if(card[j] == card[i]){
                card[i] = rand()%40;
                j = 0;
            }
        }
    }

    for(i = 0; i < 4; i++){
    	bzero(clientes[i].mao, 7);
    	for(j = 0; j < 3; j++){
    		strcat(clientes[i].mao, baralho[card[k]].nome);
    		k++;
    	}
    }
}

void entregar(jogador clientes[4], char mensagem[32]){
/* Esta funçaõ realiza o envio de uma mensagem padrao para todos os clientes */

	int i;

	for(i = 0; i < 4; i++){
		setToken(mensagem, 0, 0, clientes[i].id);
		setToken(mensagem, 1, 1, clientes[i].equipe);
		setToken(mensagem, 4, 9, clientes[i].mao);
		write(clientes[i].porta, mensagem, 31);
		sleep(1);
	}
}

int getValor(char *nome, carta baralho[40]){
/* Retorna o valor de uma carta com base no nome da mesma */

	int i;
	for(i = 0; i < 40; i++){
		if(strcmp(baralho[i].nome, nome) == 0)
			return baralho[i].valor;
	}
	if(i == 40)
		return 0;
}

char* getToken(char mensagem[32], int inicio, int fim, char *token){
/* Retorna um trecho específico da mensagem delimitado por 'inicio' e 'fim' */

	bzero(token,8);
	int i, j = 0;
	for(i = inicio ; i <= fim; i++){
		token[j] = mensagem[i];
		j++;
	}

	return token;
}

void setToken(char mensagem[32], int inicio, int fim, char *token){
/* Altera um trecho especifico da mensagem delimitado por 'inicio' e 'fim' */

	int i, j = 0;
	for(i = inicio; i <= fim; i++){
		mensagem[i] = token[j];
		j++;
	}
}

int vencTurno(char mensagem[32], carta baralho[40]){
/* Retorna o id do jogador vencedor do turno */
	char token[3];
	int i, carta[4];

	carta[0] = getValor(getToken(mensagem, 22, 23, token), baralho);
	carta[1] = getValor(getToken(mensagem, 24, 25, token), baralho);
	carta[2] = getValor(getToken(mensagem, 26, 27, token), baralho);
	carta[3] = getValor(getToken(mensagem, 28, 29, token), baralho);

	int idMaior = 0, maior = carta[0];

	for(i = 1; i < 4; i++){
		if(carta[i] > maior){
			maior = carta[i];
			idMaior = i;
		}
		else if( carta[i] == maior){
			if((i%2) != (idMaior%2))
				idMaior = 10 + i; // Caso der empate
		}
	}

	sleep(2);
	return idMaior;
}

int vencRodada(char mensagem[32], char *placarJogo){
/* Retorna 1 se uma equipe ja venceu a rodada, e atualiza o placar do jogo */

	int i, cont_A = 0, cont_B = 0, cont_ = 0, cont_jogadas = 0;
	char placarRodada[3];
	char valorRodada[3];
	int jogo, rodada;

	strcpy(placarRodada, getToken(mensagem, 14, 16, placarRodada));
	printf("O placar da rodada esta: %s\n\n",placarRodada );

	for(i = 0; i < 3; i++){
		if(placarRodada[i] != '0'){
			cont_jogadas++;
		}
		if(placarRodada[i] == 'a'){
			cont_A++;
		}
		if(placarRodada[i] == 'b'){
			cont_B++;
		}
		if(placarRodada[i] == '-'){
			cont_++;
		}
	}




	if(cont_jogadas >= 2){
		if(cont_A > cont_B){
			getToken(mensagem, 17, 18, valorRodada);
			getToken(mensagem, 10, 11, placarJogo);
			rodada = atoi(valorRodada);
			jogo = atoi(placarJogo);
			jogo += rodada;
			sprintf(placarJogo, "%d", jogo);

			setToken(mensagem, 10, 11, placarJogo); // Atualizando o placar do jogo
			printf("A equipe A venceu a rodada!\n\n");
			strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));
			return 1;
		}
		else if(cont_B > cont_A){
			getToken(mensagem, 17, 18, valorRodada);
			getToken(mensagem, 12, 13, placarJogo);
			rodada = atoi(valorRodada);
			jogo = atoi(placarJogo);
			jogo += rodada;
			sprintf(placarJogo, "%d", jogo);

			setToken(mensagem, 12, 13, placarJogo); // Atualizando o placar do jogo
			printf("A equipe B venceu a rodada!\n\n");
			strcpy(placarJogo, getToken(mensagem, 10, 11, placarRodada));
			strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));
			return 1;
		}
		else if( (cont_A == cont_B) && (cont_ >= 1)){
			for(i = 0; i < 3; i++){
				if(placarRodada[i] == 'a'){
					getToken(mensagem, 17, 18, valorRodada);
					getToken(mensagem, 10, 11, placarJogo);
					rodada = atoi(valorRodada);
					jogo = atoi(placarJogo);
					jogo += rodada;
					sprintf(placarJogo, "%d", jogo);

					setToken(mensagem, 10, 11, placarJogo); // Atualizando o placar do jogo
					printf("A equipe A venceu a rodada!\n\n");
					strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));
					return 1;
				}
				else if(placarRodada[i] == 'b'){
					getToken(mensagem, 17, 18, valorRodada);
					getToken(mensagem, 12, 13, placarJogo);
					rodada = atoi(valorRodada);
					jogo = atoi(placarJogo);
					jogo += rodada;
					sprintf(placarJogo, "%d", jogo);

					setToken(mensagem, 12, 13, placarJogo); // Atualizando o placar do jogo
					printf("A equipe B venceu a rodada!\n\n");
					strcpy(placarJogo, getToken(mensagem, 10, 11, placarRodada));
					strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));
					return 1;
				}
			}
		}
	}

	return 0;
}

int vencJogo(char mensagem [32]){
/* Retorna 1 caso alguma equipe tenha vencido o jogo(atingido 12 pts) */

	char placar[5], aux[3], aux2[3];
	int pA=0, pB=0;

	getToken(mensagem, 10, 13, placar);
	getToken(placar, 0, 1, aux);
	getToken(placar, 2, 3, aux2);

	pA = atoi(aux);
	pB = atoi(aux2);

	if(pA > 11){
		printf("\nA equipe A venceu o jogo!\n");
		return 1;
	}

	if(pB > 11){
		printf("\nA equipe B venceu o jogo!\n");
		return 1;
	}
	return 0;
}

int maoDe11(char *placarJogo){
	char a[3], b[3];

	getToken(placarJogo, 0, 1, a);
	getToken(placarJogo, 2, 3, b);

	if((strcmp(a, "11") == 0) ||(strcmp(b, "11") == 0))
		return 1;
	return 0;
}

void unirMsg(char mensagem[32], char *vez, char *rodada, char *placarJogo, char *placarRodada,
			 char *valorRodada, char *question, char *eqQuestion,
			 char *respQuestion, char *mesa, char *virada){
/* Esta função reune todas strings em uma unica mensagem */
	bzero(mensagem, 32);
 	strcpy(mensagem, "00");
	strcat(mensagem, vez);
	strcat(mensagem, rodada);
	strcat(mensagem, "000000");
	strcat(mensagem, placarJogo);
	strcat(mensagem, placarRodada);
	strcat(mensagem, valorRodada);
	strcat(mensagem, question);
	strcat(mensagem, eqQuestion);
	strcat(mensagem, respQuestion);
	strcat(mensagem, mesa);
	strcat(mensagem, "\n");
}

void broadCast(char mensagem[32], jogador clientes[4]){
/* Envia uma mesma mensagem para todos os clientes */
	int i;

	setToken(mensagem, 2, 2, "0"); // Indica que não é a vez de ninguem
	for(i = 0; i < 4; i++){
		write(clientes[i].porta, mensagem, 31);
	}
}
