# Jogo de Truco em rede
Projeto apresentado ao curso de Ciência da Computação, da
Universidade Federal de São João del Rei, como requisito parcial 
para obtenção da nota final da disciplina de Redes de Computadores.

Para o bom funcionamento deste projeto, recomendamos que o mesmo seja executado em ambiente linux, bem como que suas dependências estejam instaladas no sistema. 
Sendo elas: 
- biblioteca "pygame" : Pode ser instalada por meio do gerenciador de pacotes "pip", através do comando:

      sudo pip install pygame
 
Caso não tenha o gerenciador "pip" instalado, o mesmo pode ser obtido digitando-se o comando:

      sudo apt-get install pip

## Executando
Execução do servidor:
Para executar o servidor, acesse a pasta "./servidor" e execute o arquivo "servidorExe":

      ./servidorExe

Execução do cliente:
O servidor irá iniciar o jogo apenas após 4 clientes estarem conectados a ele.
Caso deseje executar os 4 clientes em um mesmo computador, recomendamos que execute apenas
1 cliente com interface gráfica e os demais sem interface.
- Para executar um cliente com interface gráfica acesse a pasta Clinte_Interface:

      cd Cliente/Cliente_Interface
      
   e digite o comando:
      
      python cliente_gui.py

- Para executar um cliente sem interface gráfica acesse a pasta Cliente_Terminal:

      cd Cliente/Cliente_Terminal
  
  e digite o comando:
  
      python cliente.py

Observação: Para o cliente com interface configure o ip e a porta do servidor 
no arquivo "config" presente na pasta "./Cliente/Cliente_Iterface" .

### Desenvolvido por:
![](https://github.com/Exterminus.png?size=100)
Carlos Magno ([github](https://github.com/Exterminus))

![](https://github.com/Lucasgscruz.png?size=100)
Lucas Cruz ([github](https://github.com/lucasgscruz))
