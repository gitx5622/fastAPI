from fastapi import FastAPI
from . import products, users, auth

app = FastAPI()

app.include_router(products.router)
app.include_router(users.router)
app.include_router(auth.router)



