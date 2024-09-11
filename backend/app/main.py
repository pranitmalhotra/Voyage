from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.db import Base, engine
from routes import form

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(form.router)