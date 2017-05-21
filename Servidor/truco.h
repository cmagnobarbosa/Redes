typedef struct carta{
	char nome[3];
	int valor;
} carta;

typedef struct jogador{
	int porta;
	char id[2];
	char equipe[2];
	char mao[7];
} jogador;

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

void truco (char mensagem[32], char *valorRodada);

void mudaPlacar(char *placarJogo, char *valorRodada, char *equipe);

void unirMsg(char mensagem[32], char *vez, char *rodada, char *placarJogo, char *placarRodada,
			 char *valorRodada, char *question, char *eqQuestion,
			 char *respQuestion, char *mesa, char *virada);

void broadCast(char mensagem[32], jogador clientes[4]);
