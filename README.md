# CryptoBridge
Pequena API de consulta de preços de criptomoedas em diversas linguagens.

## Sobre:
CriptoBridge é um pequeno projeto para consultar dados de criptomoedas de diversas exchanges e padronizar respostas para o usuário.

## Objetivo:
Em um certo dia, estava pensando em alguma aplicação que poderia desenvolver para praticar algumas linguagens que uso com frequência ou até mesmo aprender um pouco mais sobre alguma outra que não exercitei por tanto tempo assim. Pensei, então, em algum tema que eu gostasse de trabalhar. Não queria fazer nada com livros, bancos e agendas e, por gostar de criptomoedas, me fiz uma pergunta:

*"Por que não construir uma API para consultar os preços de vários lugares e retornar a informação para o usuário?"*

E assim a ideia surgiu para mim. Isso combina duas coisas que adoro: programação e criptomoedas.

## Recursos:
- Arquitetura simples para consulta. Basta indicar o nome da exchange desejada e o par desejado;
- Sistema básico de cache de informações para evitar **429** nas APIs de consulta;
- Retorno padronizado para o usuário. Cada exchange retorna informações de um jeito. A CryptoBridge trata isso e retorna uma resposta de forma padronizada.
