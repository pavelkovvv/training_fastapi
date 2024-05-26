import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_users import FastAPIUsers
from redis import asyncio as aioredis

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from models.models import user
from src.operations.router import router_operation
from src.tasks.router import router as tasks_router


app = FastAPI(
    title='Trading App'
)

fastapi_users = FastAPIUsers[user, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

app.include_router(router_operation)
app.include_router(tasks_router)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

if __name__ == '__main__':
    uvicorn.run(app)
