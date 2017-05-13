#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
void unir(char *msg, char *token, char *token2){
	bzero(msg, 32);
	strcat(msg, token);
	strcat(msg, token2);
	strcat(msg,"\n");
	strcat(msg,"\n");
	strcat(msg,"\n");
}

int main(){

	char msg[32] = "111111111111111111111";
	char token[7] = "lucas";
	char token2[4] = "Alo";

	unir(msg, token, token2);

	printf("Token vale: %s\n", msg );





	return 0;
}































