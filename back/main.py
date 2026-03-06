from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pages.interpark_statistic import router as interpark_router

app = FastAPI(title="Interpark Main API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://192.168.0.105:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": True}

app.include_router(interpark_router)