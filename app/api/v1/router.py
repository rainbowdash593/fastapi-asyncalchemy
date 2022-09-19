from fastapi import APIRouter

from app.api.v1.endpoints import users, auth

router = APIRouter()
router.include_router(users, prefix="/users", tags=["users"])
router.include_router(auth, prefix="/auth", tags=["auth"])