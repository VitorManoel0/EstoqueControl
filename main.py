from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import asyncio
from datetime import datetime
from routes import clients, products, orders, budget

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(clients.router)
app.include_router(products.router)
app.include_router(orders.router)
app.include_router(budget.router)

async def timer_ping():
    """Timer simples que roda a cada 5 minutos"""
    while True:
        print(f"🔔 Ping timer executado às {datetime.now()}")
        await asyncio.sleep(300)  # 5 minutos = 300 segundos
        # await asyncio.sleep(30)  # 5 minutos = 300 segundos


@app.on_event("startup")
async def startup_event():
    """Inicia o timer quando a aplicação inicializa"""
    print("🚀 Iniciando timer de 5 minutos...")
    asyncio.create_task(timer_ping())

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=7894)
