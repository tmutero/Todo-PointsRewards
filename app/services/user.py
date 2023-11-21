from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from datetime import timedelta

from jose import JWTError, jwt
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.daos import user
from app.db import get_session
from app.models.user import User as UserModel
from app.schemas.token import Token, TokenData
from app.schemas.user import ChangePasswordIn, UserIn, UserLogin, UserOut
from app.services.utils import UtilsService, oauth2_scheme
from app.settings import settings
from app.services.permission import PermissionService
from app.services.role import RoleService




class UserService:
    @staticmethod
    async def register_user(user_data: UserIn, session: AsyncSession):
        user_exist = await UserService.user_email_exists(session, user_data.email)

        if user_exist:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with the given email already exists!!!",
            )

        user_data.password = UtilsService.get_password_hash(user_data.password)
        new_user = await user.UserDao(session).create(user_data.model_dump())
        logger.info(f"New user created successfully: {new_user}!!!")
        return JSONResponse(
            content={"message": "User created successfully"},
            status_code=status.HTTP_201_CREATED,
        )

    @staticmethod
    async def authenticate_user(session: AsyncSession, form_data: UserLogin) -> UserModel | bool:
        _user = await user.UserDao(session).get_by_email(form_data.username)
       

        if not _user or not UtilsService.verify_password(form_data.password, _user.password):
            return False
        return _user

    @staticmethod
    async def user_email_exists(session: AsyncSession, email: str) -> UserModel | None:
        
        _user = await user.UserDao(session).get_by_email(email)
        return _user if _user else None

    @staticmethod
    async def login(form_data: UserLogin, session: AsyncSession) -> Token:
        _user = await UserService.authenticate_user(session, form_data)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect email or password",
            )
            
        roles  = []
    
        permissions = await PermissionService.get_permissions_by_user_id(_user.id, session)
        
    
        for x in permissions:
            _role = await RoleService.get_role_by_id(x.role_id, session)
            roles.append(_role.name)
  

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = UtilsService.create_access_token(data={"sub":_user.email,"email": _user.email,"lastname": _user.first_name, "firstname": _user.last_name,"id": _user.id,"roles": roles}, expires_delta=access_token_expires)
        
        token_data = {
            "access_token": access_token,
            "token_type": "Bearer",
        }
        return Token(**token_data)

    @staticmethod
    async def get_current_user(
        session: AsyncSession = Depends(get_session),
        token: str = Depends(oauth2_scheme),
    ) -> UserModel:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            email: str = payload.get("sub")
            if not email:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        _user = await user.UserDao(session).get_by_email(email=token_data.email)
        if not _user:
            raise credentials_exception
        return _user

    @staticmethod
    async def get_all_users(session: AsyncSession) -> list[UserOut]:
        all_users = await user.UserDao(session).get_all()
        return [UserOut.model_validate(_user) for _user in all_users]

    @staticmethod
    async def delete_all_users(session: AsyncSession):
        await user.UserDao(session).delete_all()
        return JSONResponse(
            content={"message": "All users deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def change_password(
        password_data: ChangePasswordIn,
        current_user: UserModel,
        session: AsyncSession = Depends(get_session),
    ):
        if not UtilsService.verify_password(password_data.old_password, current_user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect old password!!!",
            )
        current_user.password = UtilsService.get_password_hash(password_data.new_password)
        session.add(current_user)
        await session.commit()
        return JSONResponse(
            content={"message": "Password updated successfully!!!"},
            status_code=status.HTTP_200_OK,
        )

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession) -> UserOut:
        _user = await user.UserDao(session).get_by_id(user_id)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the given id does not exist!!!",
            )
        return UserOut.model_validate(_user)

    @staticmethod
    async def delete_user_by_id(user_id: int, session: AsyncSession):
        _user = await user.UserDao(session).delete_by_id(user_id)
        if not _user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with the given id does not exist!!!",
            )
        return JSONResponse(
            content={"message": "User deleted successfully!!!"},
            status_code=status.HTTP_200_OK,
        )
