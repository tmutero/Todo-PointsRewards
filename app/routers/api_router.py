from fastapi import APIRouter

from app.routers import user, role, permission, tasks, achivement

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(user.router)
api_router.include_router(permission.router)
api_router.include_router(role.router)
api_router.include_router(tasks.router)
api_router.include_router(achivement.router)





