"""
https://habr.com/ru/post/580866/

uvicorn main:app --host 0.0.0.0 --port 8000

https://github.com/fastapi-admin/fastapi-admin
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from pairs.api.pairs import pairs_router
from pairs.api.visits import visits_router
from roles.api.roles import roles_router
from roles.api.user_roles import user_roles_router
from users.api.token import token_router
from users.api.users import users_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(token_router, prefix='/api/v1')
app.include_router(users_router, prefix='/api/v1')
app.include_router(pairs_router, prefix='/api/v1')
app.include_router(roles_router, prefix='/api/v1')
app.include_router(visits_router, prefix='/api/v1')
app.include_router(user_roles_router, prefix='/api/v1')
