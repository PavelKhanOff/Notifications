from fastapi import APIRouter, Depends, status, Header
from .user_dal import UserDAL
from app.user import schemas
from starlette.responses import Response
from typing import Optional
from .dependencies import get_user_dal
from fastapi_pagination.paginator import paginate as paginate_list
from app.pagination import CustomPage as Page
from http import HTTPStatus
from fastapi.responses import JSONResponse
from app.auth.jwt_decoder import decode
from app.auth.jwt_decoder import get_superuser

router = APIRouter(tags=['User'])


@router.get("/notifications/users", response_model=Page[schemas.UserOut], status_code=200, dependencies=[Depends(get_superuser)])
async def get_users(
    user_dal: UserDAL = Depends(get_user_dal),
):
    users = await user_dal.get_users()
    return paginate_list(users)


@router.get("/notifications/users/{user_id}", response_model=schemas.UserOut, status_code=200, dependencies=[Depends(get_superuser)])
async def get_user(
        user_id: str,
        user_dal: UserDAL = Depends(get_user_dal),
        authorization: Optional[str] = Header(None)
):
    user_is_superuser = await decode(authorization)
    if user_is_superuser is None:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"message": "Auth Failed"},
        )
    user = await user_dal.get_user(user_id)
    return user


@router.post("/notifications/users/create", status_code=201, dependencies=[Depends(get_superuser)])
async def create_user(
        request: schemas.CreateUser,
        user_dal: UserDAL =
        Depends(get_user_dal)):
    user = await user_dal.create_user(
        request.id,
        request.token,
        request.username)
    return user


@router.patch("/notifications/users/{user_id}/update", status_code=201, dependencies=[Depends(get_superuser)])
async def update_user(
        user_id: str,
        request: schemas.UpdateUser,
        user_dal: UserDAL =
        Depends(get_user_dal)):
    user = await user_dal.update_user(
        user_id,
        request.id,
        request.token,
        request.username)
    return user


@router.delete('/notifications/users/{user_id}/delete', status_code=HTTPStatus.NO_CONTENT, dependencies=[Depends(get_superuser)])
async def delete_user(
    user_id: str,
    user_dal: UserDAL = Depends(get_user_dal),
):
    user = await user_dal.get_user(user_id)
    if not user:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Пользователь не найден"},
        )
    await user_dal.delete_user(user_id)
    return Response(status_code=204)
