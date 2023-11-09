from fastapi import HTTPException
import json

# Função que cria o estado inicial da entrega
def create_delivery(state, event):
    data = json.loads(event.data)
    return {
        "id": event.delivery_id,
        "budget": int(data["budget"]),
        "notes": data["notes"],
        "status": "ready"
    }


# Função que inicia a entrega
def start_delivery(state, event):
    if state['status'] != 'ready':
        raise HTTPException(status_code=400, detail="Delivery already started")

    return state | {
        "status": "active"
    }


# Função que coleta os produtos
def pickup_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] - int(data['purchase_price']) * int(data['quantity'])

    if new_budget < 0:
        raise HTTPException(status_code=400, detail="Not enough budget")

    return state | {
        "budget": new_budget,
        "purchase_price": int(data['purchase_price']),
        "quantity": int(data['quantity']),
        "status": "collected"
    }


# Função que entrega os produtos
def deliver_products(state, event):
    data = json.loads(event.data)
    new_budget = state["budget"] + int(data['sell_price']) * int(data['quantity'])
    new_quantity = state["quantity"] - int(data['quantity'])

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail="Not enough quantity")

    return state | {
        "budget": new_budget,
        "sell_price": int(data['sell_price']),
        "quantity": new_quantity,
        "status": "completed"
    }


# Função que aumenta o orçamento
def increase_budget(state, event):
    data = json.loads(event.data)
    state['budget'] += int(data['budget'])
    return state


# Dicionário que mapeia os tipos de eventos para as funções que os consomem
CONSUMERS = {
    "CREATE_DELIVERY": create_delivery,
    "START_DELIVERY": start_delivery,
    "PICKUP_PRODUCTS": pickup_products,
    "DELIVER_PRODUCTS": deliver_products,
    "INCREASE_BUDGET": increase_budget,
}