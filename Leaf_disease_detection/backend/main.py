from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from  api.v1 import predict
from  api.v1 import health
from  api.v1 import recommendation

app = FastAPI(title="Leaf Disease Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(predict.router, prefix="/api/v1")
app.include_router(recommendation.router, prefix="/api/v1")
