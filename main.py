import os
import json
import consumers
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from redis_om import get_redis_connection, HashModel

app = FastAPI()
app.mount("/static", StaticFiles(directory="react-events/build/static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)


class Delivery(HashModel):
    budget: int = 0
    notes: str = ''

    class Meta:
        database = redis


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = redis

'Esta rota retorna o arquivo index.html do diretório de build do projeto React.'
@app.get("/")
async def read_index():
    return FileResponse("react-events/build/index.html")

'''
Esta rota retorna o estado de uma entrega específica. 
Se o estado já estiver armazenado no Redis, ele é retornado diretamente. Caso contrário, o estado é construído chamando a função build_state, armazenado no Redis e então retornado.
'''
@app.get('/deliveries/{pk}/status')
async def get_state(pk: str):
    state = redis.get(f'delivery:{pk}')

    if state is not None:
        return json.loads(state)

    state = build_state(pk)
    redis.set(f'delivery:{pk}', json.dumps(state))
    return state

'''
Esta função constrói o estado de uma entrega processando todos os eventos associados a ela em ordem. 
Cada evento é processado por uma função específica definida no módulo consumers, que é passada o estado atual e o evento e retorna o estado atualizado.
'''
def build_state(pk: str):
    pks = Event.all_pks()
    all_events = [Event.get(pk) for pk in pks]
    events = [event for event in all_events if event.delivery_id == pk]
    state = {}

    for event in events:
        state = consumers.CONSUMERS[event.type](state, event)

    return state

'''
Esta rota cria uma nova entrega e um evento associado. Ela recebe um objeto JSON no corpo da solicitação com informações sobre a entrega e o evento, 
cria instâncias dos modelos Delivery e Event com essas informações, salva-os no Redis, atualiza o estado da entrega e retorna o estado atualizado.
'''
@app.post('/deliveries/create')
async def create(request: Request):
    body = await request.json()
    delivery = Delivery(budget=body['data']['budget'], notes=body['data']['notes']).save()
    event = Event(delivery_id=delivery.pk, type=body['type'], data=json.dumps(body['data'])).save()
    state = consumers.CONSUMERS[event.type]({}, event)
    redis.set(f'delivery:{delivery.pk}', json.dumps(state))
    return state

'''
 Esta rota recebe um evento associado a uma entrega existente. Ela recebe um objeto JSON no corpo da solicitação com informações sobre o evento, 
 recupera o estado atual da entrega, cria uma instância do modelo Event com as informações do evento, atualiza o estado da entrega e retorna o estado atualizado.
'''
@app.post('/event')
async def dispatch(request: Request):
    body = await request.json()
    delivery_id = body['delivery_id']
    state = await get_state(delivery_id)
    event = Event(delivery_id=delivery_id, type=body['type'], data=json.dumps(body['data'])).save()
    new_state = consumers.CONSUMERS[event.type](state, event)
    redis.set(f'delivery:{delivery_id}', json.dumps(new_state))
    return new_state