from fastapi import FastAPI
from .database import Base, engine
from .routers import blueprints, contracts
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Contract Management Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)

app.include_router(blueprints.router)
app.include_router(contracts.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
