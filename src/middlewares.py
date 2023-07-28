from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def set_cors_middleware(app: FastAPI):
    """CORS settings allow the frontend part to send requests to the API."""
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
