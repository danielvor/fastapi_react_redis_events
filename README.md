# Projeto de Arquitetura Orientada a Eventos com FastAPI, React e Redis

Este projeto é um exemplo de como implementar uma arquitetura orientada a eventos, construindo um projeto do mundo real usando FastAPI, React e Redis. Um sistema orientado a eventos é uma forma comum de configurar software. Na arquitetura orientada a eventos, os manipuladores de eventos são registrados para eventos específicos. Quando ocorre um evento, os manipuladores são invocados.

## Requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- Redis 6 ou superior

## Instalação

- Clone o repositório do github:

```bash
git clone https://github.com/danielvor/FastAPI_Redis.git
```

- Entre na pasta do projeto:

```bash
cd FASTAPI_REDIS
```

- Crie um ambiente virtual, ative-o e Instale as dependências do Python:

```bash
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
```

- Entre na pasta react-events e instale as dependências do Node.js:

```bash
cd react-events && npm install
```

## Configuração

- Crie um banco de dados no Redis e anote o endereço, a porta e a senha.
- Dentro do arquivo `.env` adicione suas credenciais:

```bash
REDIS_HOST=seu-endereco-do-redis
REDIS_PORT=sua-porta-do-redis
REDIS_PASSWORD=sua-senha-do-redis
```

## Execução

- Em um terminal, execute o servidor FastAPI com o comando:

```bash
uvicorn main:app --reload
```

Esse comando inicia o servidor na porta 8000 e habilita o modo de recarga automática, que reinicia o servidor sempre que um arquivo é modificado.

- Em outro terminal, execute o cliente React com o comando:

```bash
npm start
```

Esse comando inicia o cliente na porta 3000 e abre o navegador na página inicial do projeto.

- Agora você pode testar o projeto e ver como os eventos são gerados e manipulados pelo FastAPI e pelo React.