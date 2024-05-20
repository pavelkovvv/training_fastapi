import uvicorn
from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from models.models import user


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

if __name__ == '__main__':
    uvicorn.run(app)