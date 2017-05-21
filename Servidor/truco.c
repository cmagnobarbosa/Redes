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
	int i = 0, j = 0, k = 0;
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
	//char zero[2] ;
	//int jogo, rodada;

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

	int rodada, valorPlacar;
	char placar[3];
	char aux[2] ;

	getToken(mensagem, 17, 18, valorRodada);
	rodada = atoi(valorRodada);

	// if(strcmp(equipe, "a") == 0){
	// 	getToken(placarJogo, 0, 1, placar);
	// 	valorPlacar = atoi(placar);
	// 	valorPlacar += rodada;
	// 	sprintf(aux, "%d", valorPlacar);

	// 	if(valorPlacar < 10){
	// 		strcpy(placar, "0");
	// 		strcat(placar, aux);
	// 	}
	// 	else{
	// 		strcpy(placar, aux);
	// 	}	 
	// 	setToken(placarJogo, 0, 1, placar);

	// }
	// else if(strcmp(equipe, "b") == 0){
	// 	getToken(placarJogo, 2, 3, placar);
	// 	valorPlacar = atoi(placar);
	// 	valorPlacar += rodada;
	// 	sprintf(aux, "%d", valorPlacar);
	// 	if(valorPlacar < 10){
	// 		strcpy(placar, "0");
	// 		strcat(placar, aux);
	// 	}
	// 	else{
	// 		strcpy(placar, aux);
	// 	}
	// 	setToken(placarJogo, 2, 3, placar);
	// }

	
		

	if(cont_jogadas >= 2){
		if(cont_A > cont_B){
			// getToken(mensagem, 17, 18, valorRodada);
			// getToken(mensagem, 10, 11, placarJogo);   
			// rodada = atoi(valorRodada);
			// jogo = atoi(placarJogo);
			// jogo += rodada; 
			// sprintf(zero, "%d", jogo);
			// if(jogo < 10){
			// 	strcpy(placarJogo, "0");
			// 	strcat(placarJogo, zero);
			// }
			// else{
			// 	strcat(placarJogo, zero);
			// }

			// setToken(mensagem, 10, 11, placarJogo); // Atualizando o placar do jogo
			// bzero(placarJogo, 4);
			// strcpy(placarJogo, getToken(mensagem, 10, 11, placarRodada));
			// strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));
			

			getToken(placarJogo, 0, 1, placar);
			valorPlacar = atoi(placar);
			valorPlacar += rodada;
			sprintf(aux, "%d", valorPlacar);

			if(valorPlacar < 10){
				strcpy(placar, "0");
				strcat(placar, aux);
			}
			else{
				strcpy(placar, aux);
			}	 
			setToken(placarJogo, 0, 1, placar);

			printf("A equipe A venceu a rodada!\n\n");
			return 1;
		}
		else if(cont_B > cont_A){
			// getToken(mensagem, 17, 18, valorRodada);
			// getToken(mensagem, 12, 13, placarJogo);
			// rodada = atoi(valorRodada);
			// jogo = atoi(placarJogo);
			// jogo += rodada;
			// sprintf(zero, "%d", jogo);
			// if(jogo < 10){
			// 	strcpy(placarJogo, "0");
			// 	strcat(placarJogo, zero);
			// }
			// else{
			// 	strcat(placarJogo, zero);
			// }
			// setToken(mensagem, 12, 13, placarJogo); // Atualizando o placar do jogo
			// bzero(placarJogo, 4);
			// strcpy(placarJogo, getToken(mensagem, 10, 11, placarRodada));
			// strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));



			getToken(placarJogo, 2, 3, placar);
			valorPlacar = atoi(placar);
			valorPlacar += rodada;
			sprintf(aux, "%d", valorPlacar);
			if(valorPlacar < 10){
				strcpy(placar, "0");
				strcat(placar, aux);
			}
			else{
				strcpy(placar, aux);
			}
			setToken(placarJogo, 2, 3, placar);


			printf("A equipe B venceu a rodada!\n\n");
			return 1;
		}
		else if( (cont_A == cont_B) && (cont_ >= 1)){
			for(i = 0; i < 3; i++){
				if(placarRodada[i] == 'a'){
					// getToken(mensagem, 17, 18, valorRodada);
					// getToken(mensagem, 10, 11, placarJogo);   
					// rodada = atoi(valorRodada);
					// jogo = atoi(placarJogo);
					// jogo += rodada; 
					// sprintf(zero, "%d", jogo);
					// if(jogo < 10){
					// 	strcpy(placarJogo, "0");
					// 	strcat(placarJogo, zero);
					// }
					// else{
					// 	strcpy(placarJogo, zero);
					// }
					// setToken(mensagem, 10, 11, placarJogo); // Atualizando o placar do jogo
					// bzero(placarJogo, 4);
					// strcpy(placarJogo, getToken(mensagem, 10, 11, placarRodada));
					// strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));




					getToken(placarJogo, 0, 1, placar);
					valorPlacar = atoi(placar);
					valorPlacar += rodada;
					sprintf(aux, "%d", valorPlacar);

					if(valorPlacar < 10){
						strcpy(placar, "0");
						strcat(placar, aux);
					}
					else{
						strcpy(placar, aux);
					}	 
					setToken(placarJogo, 0, 1, placar);
					
					printf("A equipe A venceu a rodada!\n\n");
					return 1;
				}
				else if(placarRodada[i] == 'b'){
					// getToken(mensagem, 17, 18, valorRodada);
					// getToken(mensagem, 12, 13, placarJogo);
					// rodada = atoi(valorRodada);
					// jogo = atoi(placarJogo);
					// jogo += rodada;
					// sprintf(zero, "%d", jogo);
					// if(jogo < 10){
					// 	strcpy(placarJogo, "0");
					// 	strcat(placarJogo, zero);
					// }
					// else{
					// 	strcat(placarJogo, zero);
					// }
					// setToken(mensagem, 12, 13, placarJogo); // Atualizando o placar do jogo
					// bzero(placarJogo, 4);
					// strcpy(placarJogo, getToken(mensagem, 10, 11, placarRodada));
					// strcat(placarJogo, getToken(mensagem, 12, 13, placarRodada));



					getToken(placarJogo, 2, 3, placar);
					valorPlacar = atoi(placar);
					valorPlacar += rodada;
					sprintf(aux, "%d", valorPlacar);
					if(valorPlacar < 10){
						strcpy(placar, "0");
						strcat(placar, aux);
					}
					else{
						strcpy(placar, aux);
					}
					setToken(placarJogo, 2, 3, placar);


					
					printf("A equipe B venceu a rodada!\n\n");
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

	printf("Placar do jogo -------- %s\n", placar);

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

void truco (char mensagem[32], char *valorRodada){
/* Aumenta o valor da rodada caso haja um pedido de truco */
	int rodada;
	char aux[2];

	rodada = atoi(valorRodada);

	if(rodada == 1){
		rodada = 3;
	}
	else if(rodada == 3){
		rodada = 6;
	}
	else if(rodada == 6){
		rodada = 9;
	}
	else if(rodada == 9){
		rodada = 12;
	}
	bzero(valorRodada, 3);
	sprintf(aux, "%d", rodada);

	if(rodada >= 10){
		strcat(valorRodada, aux);
		setToken(mensagem, 17, 18, aux);
	}
	else{
		strcpy(valorRodada, "0");
		strcat(valorRodada, aux);
		setToken(mensagem, 17, 18, valorRodada);
	}
}

void mudaPlacar(char *placarJogo, char *valorRodada, char *equipe){
/* Muda o plcar do jogo, caso alguma equipe fuja de um pedido de truco */

	int rodada, valorPlacar;
	char placar[3];
	char aux[2] ;
	rodada = atoi(valorRodada);

	if(strcmp(equipe, "a") == 0){
		getToken(placarJogo, 0, 1, placar);
		valorPlacar = atoi(placar);
		valorPlacar += rodada;
		sprintf(aux, "%d", valorPlacar);

		if(valorPlacar < 10){
			strcpy(placar, "0");
			strcat(placar, aux);
		}
		else{
			strcpy(placar, aux);
		}	 
		setToken(placarJogo, 0, 1, placar);

	}
	else if(strcmp(equipe, "b") == 0){
		getToken(placarJogo, 2, 3, placar);
		valorPlacar = atoi(placar);
		valorPlacar += rodada;
		sprintf(aux, "%d", valorPlacar);
		if(valorPlacar < 10){
			strcpy(placar, "0");
			strcat(placar, aux);
		}
		else{
			strcpy(placar, aux);
		}
		setToken(placarJogo, 2, 3, placar);
	}

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
