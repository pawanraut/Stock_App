from pydantic import BaseModel
from typing import Optional, List, Any

# -----------------------------
# Access Token Schemas
# -----------------------------
class RequestToken(BaseModel):
    request_token: str

class AccessTokenResponse(BaseModel):
    status: str
    access_token: str

# -----------------------------
# Order Schemas
# -----------------------------
class OrderRequest(BaseModel):
    tradingsymbol: str
    quantity: int
    price: float

class ModifyOrderRequest(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None

class OrderResponse(BaseModel):
    status: str
    order_id: str
    data: Optional[Any] = None

class OrdersListResponse(BaseModel):
    orders: List[Any]
