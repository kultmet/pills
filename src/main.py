from fastapi import FastAPI
from fastapi.responses import Response
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from src.pills.routers import pills_router

origins = ["*"]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = FastAPI(title="Wagon Lots API", middleware=middleware)

app.include_router(pills_router)
