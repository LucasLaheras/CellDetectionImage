# CellDetectionImage
Interface gráfica feita no TKinter para segmentação de imagens médicas e biológicas usando algoritmos bio-inspirados

# Execução
- Certifique-se se está instalado a versão 3.6 do Pyhton.
- Instale os seguintes pacotes: TKinter, numpy, PIL, ITK e opencv-python.
- Execute o arquivo Main.py.

# Como Utilizar

![alt text](Images/InterfaceGrafica.png)

Para utilizar as funções da interface é preciso clicar na imagem da esquerda na região que está segmentada de forma errada e com _mouse_ passar por cima da área da imagem à direita com a opção caneta ou borracha selecionada (A e B da Figura) e após concluído clicar em "Aplicar" (botão referente a letra F na Figura), assim, modificando a imagem da esquerda para obter a segmentação correta. A barra de rolagem C determina o tamanho da borracha ou caneta selecionada. O botão E altera a imagem da esquerda para a imagem que foi inicialmente gerada pelo algorítimo. Para facilitar para o usuário demarcar a região, está sendo implementada a função de zoom da imagem utilizando a barra de rolagem D.


