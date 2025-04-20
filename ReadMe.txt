Monitor de logs

O Projeto tem um monito de arquivos de log, que detecta anomalias específicas dentro de arquvios log e as salva 

Basta ter [Docker instalado](https://docs.docker.com/get-docker/).  
Não é necessário configurar Python nem dependências.


Os requisitos para rodar os testes estao em requirements.txt

para rodar o projeto no seu computador basta rodar dois comandos simples:

- docker build -t monitor-anomalias (para construir a imagem docker)
- docker run --rm -v "$PWD":/app monitor-anomalias (para rodar o projeto)

Para rodar os tests:
 - docker run --rm monitor-anomalias pytest


Não faz parte do teste mas tomei a liberdade de versionar o projeto com git (espero que não tenha problema)
para caso tenha algum problema na transferencia dos arquivos, pode clonar o repositorio atraves do link:

- https://github.com/gustaOliveira0/monitor-anomalias



