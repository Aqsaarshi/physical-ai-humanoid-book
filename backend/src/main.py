import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import chat

# -------------------- FastAPI App Initialization -------------------- #
app = FastAPI()

# -------------------- CORS Middleware -------------------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Include Routers -------------------- #
# Router prefix added here
app.include_router(chat.router, prefix="/api/chat")


# -------------------- Root Endpoint -------------------- #
@app.get("/")
def root():
    return {"status": "Backend running"}
