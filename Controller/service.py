from kiteconnect import KiteConnect
from Component.config import API_KEY, API_SECRET
from Component.database import get_connection, release_connection
from psycopg2.extras import RealDictCursor

kite = KiteConnect(api_key=API_KEY)



def save_access_token(token: str):
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("INSERT INTO access_tokens (token) VALUES (%s)", (token,))
            conn.commit()
    finally:
        release_connection(conn)



def get_latest_token():
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT token FROM access_tokens ORDER BY id DESC LIMIT 1")
            row = cur.fetchone()
            return row["token"] if row else None
    finally:
        release_connection(conn)




def generate_access_token(request_token: str):
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    access_token = data["access_token"]
    kite.set_access_token(access_token)
    save_access_token(access_token)
    return access_token



def load_access_token():
    token = get_latest_token()
    if token:
        kite.set_access_token(token)
    return token



def generate_and_save_token(request_token: str):
    access_token = generate_access_token(request_token)
    return {"access_token": access_token}



def get_dummy_user_id():

    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id FROM users LIMIT 1")
            row = cur.fetchone()
            return row["id"]
    finally:
        release_connection(conn)



def place_order(tradingsymbol: str, quantity: int, price: float, transaction_type: str):
    order_id = kite.place_order(
        variety=kite.VARIETY_REGULAR,
        exchange=kite.EXCHANGE_NSE,
        tradingsymbol=tradingsymbol,
        transaction_type=transaction_type,
        quantity=quantity,
        product=kite.PRODUCT_CNC,
        order_type=kite.ORDER_TYPE_LIMIT,
        price=price
    )
    user_id = get_dummy_user_id()
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                INSERT INTO orders (user_id, order_id, tradingsymbol, quantity, price, transaction_type)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, order_id, tradingsymbol, quantity, price, transaction_type))
            conn.commit()
    finally:
        release_connection(conn)
    return order_id




def modify_order(order_id: str, quantity: int = None, price: float = None):
    if quantity is None and price is None:
        raise ValueError("At least one of quantity or price must be provided")
    return kite.modify_order(
        variety=kite.VARIETY_REGULAR,
        order_id=order_id,
        quantity=quantity,
        price=price
    )

def get_orders():
    return kite.orders()
