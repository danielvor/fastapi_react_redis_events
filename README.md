# Arquitetura Orientada a Eventos com FastAPI, React e Redis

Neste README, vamos explorar os principais componentes e funcionalidades do seu sistema. Vamos lá:

## Visão Geral

O objetivo deste projeto é praticar algoritmos em Python, criando uma arquitetura orientada a objetos com os seguintes componentes:

1. **Backend com FastAPI**: Aqui, utilizamos o FastAPI para criar uma API robusta e eficiente. Ele nos permite definir rotas, gerenciar entregas e eventos associados.

2. **Frontend com React**: O React é nossa escolha para a interface do usuário. Ele nos permite criar uma experiência interativa e responsiva para os usuários.

3. **Banco de Dados Redis**: O Redis é nosso banco de dados. Ele é rápido, escalável e perfeito para armazenar informações sobre entregas e eventos.

## Estrutura do Projeto

Vamos dar uma olhada nas partes essenciais do código:

### 1. Importações

No arquivo `main.py`, começamos importando várias bibliotecas essenciais:

- **FastAPI**: Nosso framework para criar a API.
- **Middleware CORS**: Para lidar com solicitações de origens específicas.
- **Conexão Redis**: Estabelecemos uma conexão com o banco de dados.
- **HashModel**: Usado para modelar e armazenar informações.
- **FileResponse**: Para servir arquivos estáticos.
- **StaticFiles**: Montamos um diretório estático para servir arquivos.

### 2. Configuração do Aplicativo

Criamos uma instância do FastAPI e configuramos o diretório estático para servir arquivos do projeto React. Além disso, adicionamos um middleware CORS para permitir solicitações de origens específicas.

### 3. Conexão com o Redis

Usamos a função `get_redis_connection` para estabelecer uma conexão com o banco de dados Redis. Isso nos permite armazenar e recuperar informações sobre entregas e eventos.

### 4. Definição de Modelos

Criamos duas classes: Delivery e Event. 
Essas classes são utilizadas para modelar e armazenar informações relacionadas a entregas e eventos no banco de dados Redis.

- **Delivery**: Modela informações sobre entregas.
- **Event**: Armazena detalhes sobre eventos associados.

### 5. Rotas

As rotas são essenciais para nossa API:

- **@app.get("/")**: Esta rota retorna o arquivo `index.html` do diretório de build do projeto React.
- **@app.get('/deliveries/{pk}/status')**, **@app.post('/event')**, **@app.post('/deliveries/create')**, **@app.post('/event')**: Essas rotas gerenciam as entregas e eventos associados.
- **Função build_state**: Essa função é crucial para construir o estado do sistema.

### 6. Funções

O arquivo `consumers.py` contém funções relacionadas ao status e eventos do produto.

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