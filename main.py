from fastapi import FastAPI
from auth.router import router as auth_router
from db.base import Base
from db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="По следам — Auth Service")

app.include_router(auth_router)