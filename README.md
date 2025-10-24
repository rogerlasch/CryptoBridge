# CryptoBridge APIs

Este repositório contém implementações idênticas de uma API de agregação de dados de criptomoedas em diferentes linguagens de programação. As APIs foram desenvolvidas como projetos pessoais para estudo e aperfeiçoamento das habilidades de desenvolvimento em cada linguagem. No futuro, haverá outras implementações iguais em mais linguagens de programação diferentes.

## Caso de Uso

O CryptoBridge é uma API que atua como uma ponte (bridge) entre diferentes exchanges de criptomoedas, oferecendo uma interface unificada para consulta de dados. O sistema permite:

- **Consultar exchanges disponíveis**: Lista todas as exchanges suportadas pela API
- **Listar símbolos**: Obtém todos os pares de moedas disponíveis em uma exchange específica
- **Consultar preços**: Busca dados em tempo real de preços, volumes e outras métricas de mercado
- **Monitorar métricas**: Acompanha estatísticas de uso da API, performance e dados de acesso

### Funcionalidades Principais

1. **Agregação de Dados**: Centraliza dados de múltiplas exchanges em uma única API
2. **Interface Padronizada**: Oferece endpoints consistentes independente da exchange consultada
3. **Sistema de Cache**: Implementa cache inteligente para otimizar performance e reduzir latência
4. **Métricas Avançadas**: Coleta e apresenta estatísticas detalhadas de uso e performance
5. **Tratamento de Errors**: Padroniza respostas de erro e implementa fallbacks

### Exchanges Suportadas

- **Coinbase**: Exchange internacional com ampla variedade de criptomoedas
- **Mercado Bitcoin**: Principal exchange brasileira de criptomoedas

## Implementações Disponíveis

### Python (CryptoBridge-python)

**Importante** A versão Python roda melhor no Linux, e ainda contém diversas falhas e problemas que serão corrigidas em breve.
Implementação usando FastAPI com arquitetura limpa e moderna.

#### Tecnologias Utilizadas
- **FastAPI**: Framework web moderno e de alta performance
- **SQLAlchemy**: ORM para banco de dados
- **SQLite**: Banco de dados para métricas e cache
- **Pydantic**: Validação de dados e serialização
- **HTTPX**: Cliente HTTP assíncrono
- **Uvicorn**: Servidor ASGI de alta performance
- **aiosqlite**: Driver SQLite assíncrono
- **Pytest**: Framework de testes abrangente

#### Como Executar

```bash
# Navegar para o diretório
cd CryptoBridge-python

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
python3 main.py
```

A API estará disponível em: `http://localhost:3000`

#### Executar Testes

```bash
# Testes unitários e de integração
pytest

# Testes com coverage
pytest --cov=src

# Testes com relatório detalhado e HTML
pytest -v --cov=src --cov-report=html
```

**Nota**: O relatório HTML será gerado na pasta `htmlcov/`

#### Documentação
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

### Node.js (CryptoBridge-node)

Implementação usando Express.js com a mesma arquitetura e funcionalidades.

#### Tecnologias Utilizadas
- **Express.js**: Framework web flexível e minimalista
- **Prisma ORM**: ORM moderno com type-safety
- **SQLite**: Banco de dados para métricas e cache
- **Joi**: Validação de dados robusta
- **Axios**: Cliente HTTP
- **CORS**: Cross-Origin Resource Sharing
- **Helmet**: Segurança HTTP
- **Morgan**: Logging de requisições
- **Jest**: Framework de testes moderno
- **Supertest**: Testes de integração HTTP

#### Como Executar

```bash
# Navegar para o diretório
cd CryptoBridge-node

# Instalar dependências
npm install

# Configurar banco de dados com Prisma
npx prisma generate
npx prisma db push

# Iniciar o servidor
npm start

# Ou modo de desenvolvimento
npm run dev
```

A API estará disponível em: `http://localhost:3001`

#### Executar Testes

```bash
# Testes unitários e de integração
npm test

# Testes com coverage
npm run test:coverage
```

## Endpoints da API

### Bridge Endpoints

- `GET /` - Lista exchanges disponíveis
- `POST /symbols` - Lista símbolos de uma exchange
- `POST /tickers` - Obtém dados de preços

### Metrics Endpoints

- `GET /metrics/summary` - Resumo geral das métricas
- `GET /metrics/exchanges/top` - Top exchanges por requisições
- `GET /metrics/tickers/top` - Top tickers por requisições
- `GET /metrics/performance` - Métricas de performance da API

## Testes Manuais

O diretório `testes/` contém scripts curl para testar todos os endpoints manualmente:

```bash
cd testes

# Testar endpoint específico
bash test_exchanges.txt
bash test_symbols_coinbase.txt

# Executar todos os testes
bash run_all_tests.txt
```

## Estrutura do Projeto

```
api/
├── CryptoBridge-python/    # Implementação Python
├── CryptoBridge-node/      # Implementação Node.js
├── testes/                 # Scripts de teste manual
│   ├── jsons/             # Dados JSON para testes
│   └── test_*.txt         # Scripts curl
└── README.md              # Este arquivo
```

## Arquitetura

Ambas as implementações seguem os princípios da Clean Architecture:

- **Domain**: Entidades de negócio e regras fundamentais
- **Application**: Casos de uso e serviços de aplicação
- **Infrastructure**: Implementações técnicas (banco, cache, APIs externas)
- **Presentation**: Controllers, routers e middlewares

## Compatibilidade

As duas implementações são completamente intercambiáveis:
- Mesmos endpoints e parâmetros
- Respostas JSON idênticas
- Códigos de status HTTP consistentes
- Tratamento de erro padronizado

Isso permite alternar entre as implementações sem impacto nos clientes da API.

## Desenvolvimento Futuro

Planejo implementar esta mesma API em outras linguagens:
- Go
- Rust
- Java (Spring Boot)
- C# (.NET)
- PHP (Laravel)

Cada implementação manterá a mesma interface e funcionalidades, servindo como estudo comparativo entre diferentes tecnologias e paradigmas de programação.