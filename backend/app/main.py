from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import Base, engine
from .routers import blueprints, contracts

app = FastAPI(title="Contract Management Platform")

#  CORS — allow Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # acceptable for assignment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Health checks
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

#  DB + routers
Base.metadata.create_all(bind=engine)

app.include_router(blueprints.router)
app.include_router(contracts.router)
