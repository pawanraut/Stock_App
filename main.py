from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from Api import order
from Component import auth
from Component.database import create_tables
from Controller.service import load_access_token

app = FastAPI(title="Stock Trading Backend")


origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    create_tables()
    load_access_token()

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(order.router, prefix="/api/orders", tags=["Orders"])
