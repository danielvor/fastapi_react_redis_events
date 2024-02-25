import json

from fastapi import HTTPException


'''
Essa função é responsável por criar uma nova entrega. 
Ela recebe um estado e um evento como parâmetros, extrai os dados relevantes do evento e retorna um dicionário com informações sobre a entrega, como o ID, o orçamento, as notas e o status
'''
def create_delivery(state, event):
    data = json.loads(event.data)
    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": "ready"
    }

'''
Essa função é chamada para iniciar uma entrega. 
Ela verifica se o status da entrega é "ready" (pronta) no estado atual. Se não for, lança uma exceção HTTP com código de status 400. 
Caso contrário, atualiza o estado da entrega para "active" (ativa) e retorna o estado atualizado.
'''
def start_delivery(state, event):
    if state['status'] != 'ready':
        raise HTTPException(status_code=400, detail="Delivery already started")

    return state | {
        "status": "active"
    }

'''
Essa função é usada para registrar a coleta de produtos durante uma entrega. 
Ela recebe um estado e um evento como parâmetros, extrai os dados relevantes do evento e realiza cálculos com base no preço de compra e na quantidade de produtos coletados. 
Se o orçamento atual não for suficiente para cobrir o custo da compra, uma exceção HTTP com código de status 400 é lançada. 
Caso contrário, o estado é atualizado com as informações da compra e o status é definido como "collected" (coletado). O estado atualizado é retornado.
'''
def pickup_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] - \
        int(data['purchase_price']) * int(data['quantity'])

    if new_budget < 0:
        raise HTTPException(status_code=400, detail="Not enough budget")

    return state | {
        "budget": new_budget,
        "purchase_price": int(data['purchase_price']),
        "quantity": int(data['quantity']),
        "status": "collected"
    }

'''
Essa função é usada para registrar a entrega de produtos durante uma entrega. 
Ela recebe um estado e um evento como parâmetros, extrai os dados relevantes do evento e realiza cálculos com base no preço de venda e na quantidade de produtos entregues. 
Se a quantidade de produtos no estado atual for insuficiente para atender à entrega, uma exceção HTTP com código de status 400 é lançada. 
Caso contrário, o estado é atualizado com as informações da venda e a quantidade de produtos é atualizada. O status é definido como "completed" (concluído) e o estado atualizado é retornado.
'''
def deliver_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] + \
        int(data['sell_price']) * int(data['quantity'])
    new_quantity = state["quantity"] - int(data['quantity'])

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Not enough quantity")

    return state | {
        "budget": new_budget,
        "sell_price": int(data['sell_price']),
        "quantity": new_quantity,
        "status": "completed"
    }

'''
Essa função é usada para aumentar o orçamento de uma entrega. 
Ela recebe um estado e um evento como parâmetros, extrai o valor do orçamento do evento e adiciona esse valor ao orçamento atual no estado. 
O estado atualizado é retornado.
'''
def increase_budget(state, event):
    data = json.loads(event.data)
    state['budget'] += int(data['budget'])
    return state


CONSUMERS = {
    "CREATE_DELIVERY": create_delivery,
    "START_DELIVERY": start_delivery,
    "PICKUP_PRODUCTS": pickup_products,
    "DELIVER_PRODUCTS": deliver_products,
    "INCREASE_BUDGET": increase_budget,
}
