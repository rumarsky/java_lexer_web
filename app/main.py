from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import lex as lex_router

app = FastAPI(title="Java Lexer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(lex_router.router)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}
