from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=7894)
