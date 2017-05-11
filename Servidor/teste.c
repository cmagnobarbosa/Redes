#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct carta{
	char mao[6];
	int valor;
}carta;

int main(){
	
// int i,k;
// int mao[12];
//    srand(time(NULL));

// for(i = 0; i < 12; i++){
//        mao[i] = rand()%40;        
//        for(k = 0; k < i; k++){
//            if(mao[k] == mao[i]){
//                mao[i] = rand()%40;
//                k = 0;
//            }
//        }
//    }
//    for(i = 0; i < 12; i++)
//    	printf("%d\n", mao[i]);

 

// char sMensagem[100] = "Sr(a). ";
// char sNome[40] = "lucas geraldo";


// strcat(sMensagem, sNome);

// puts(sMensagem);
// puts(baralho.valor);

	carta baralho[1];
	bzero(baralho[0].mao, 6);

	strcat(baralho[0].mao, "kkk");
	//strcat(baralho[0].mao, "4p");
	//strcat(baralho[0].mao, "7c");


	printf("%s\n",baralho[0].mao );








return 0;
}