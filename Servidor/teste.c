#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef struct carta{
	char nome[3];
}carta;

int main(){

	carta lucas[1];
	char aux[88];
	bzero(aux,2);	
	aux[0] = 49;

	strcpy(lucas[0].nome, aux);

	printf("valor de lucas: %s\n", lucas[0].nome );

	return 0;

}





























