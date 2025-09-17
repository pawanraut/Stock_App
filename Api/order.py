from fastapi import APIRouter, HTTPException
from Controller.service import generate_and_save_token, get_orders, modify_order, place_order
from Component.schemas import RequestToken, AccessTokenResponse, OrderRequest, ModifyOrderRequest, OrderResponse, OrdersListResponse



router = APIRouter()



@router.post("/kite/token", response_model=AccessTokenResponse)
def get_kite_token(request: RequestToken):
    try:
        result = generate_and_save_token(request.request_token)
        return {"status": "success", "access_token": result["access_token"]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@router.post("/buy", response_model=OrderResponse)
def buy_stock(order: OrderRequest):
    if order.quantity <= 0 or order.price <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be positive")
    try:
        order_id = place_order(order.tradingsymbol, order.quantity, order.price, "BUY")
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))




@router.post("/sell", response_model=OrderResponse)
def sell_stock(order: OrderRequest):
    if order.quantity <= 0 or order.price <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be positive")
    try:
        order_id = place_order(order.tradingsymbol, order.quantity, order.price, "SELL")
        return {"status": "success", "order_id": order_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





@router.put("/modify/{order_id}", response_model=OrderResponse)
def modify_stock_order(order_id: str, order: ModifyOrderRequest):
    if order.quantity is None and order.price is None:
        raise HTTPException(status_code=400, detail="At least one of quantity or price must be provided")
    try:
        response = modify_order(order_id, order.quantity, order.price)
        return {"status": "success", "order_id": order_id, "data": response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))





@router.get("/orders", response_model=OrdersListResponse)
def list_orders():
    try:
        return {"orders": get_orders()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
