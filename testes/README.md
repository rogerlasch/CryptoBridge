# Testes da API CryptoBridge

Este diretório contém testes manuais para a API CryptoBridge usando curl.

## Estrutura

```
testes/
├── jsons/                  # Arquivos JSON com dados para testes POST
│   ├── symbols_coinbase.json
│   ├── symbols_mercadobitcoin.json
│   ├── symbols_invalid.json
│   ├── tickers_coinbase_btc.json
│   ├── tickers_coinbase_multiple.json
│   ├── tickers_mercadobitcoin.json
│   └── tickers_invalid.json
├── test_*.txt              # Scripts curl para cada endpoint
└── run_all_tests.txt       # Script para executar todos os testes
```

## Como usar

### 1. Iniciar a API
Primeiro, certifique-se de que a API está rodando:
```bash
# Python API (porta 3000)
cd CryptoBridge-python && python3 main.py

# OU Node.js API (porta 3001)
cd CryptoBridge-node && npm start
```

### 2. Executar testes individuais
Entre no diretório de testes e execute qualquer arquivo:
```bash
cd testes
bash test_exchanges.txt
bash test_symbols_coinbase.txt
bash test_tickers_coinbase_btc.txt
```

### 3. Executar todos os testes
```bash
cd testes
bash run_all_tests.txt
```

## Endpoints testados

### Bridge Endpoints
- `GET /` - Lista exchanges disponíveis
- `POST /symbols` - Lista símbolos de uma exchange
- `POST /tickers` - Obtém preços de tickers específicos

### Metrics Endpoints
- `GET /metrics/summary` - Resumo geral das métricas
- `GET /metrics/exchanges/top` - Top exchanges por requisições
- `GET /metrics/tickers/top` - Top tickers por requisições
- `GET /metrics/performance` - Métricas de performance

## Exemplos de resposta

### Sucesso
```json
{
  "status": 200,
  "exchanges": ["mercadobitcoin", "coinbase"]
}
```

### Erro
```json
{
  "status": 404,
  "msg": "A exchange especificada não existe no momento na bridge."
}
```

## Notas

- Os arquivos `.txt` contêm comandos curl que podem ser executados diretamente
- Os arquivos JSON em `jsons/` são referenciados pelos comandos curl usando `@jsons/arquivo.json`
- Para testar a API Node.js, altere a porta de 3000 para 3001 nos arquivos de teste