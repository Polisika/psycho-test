from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils, table, instruction, test

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(table.router, prefix="/tables", tags=["tables"])
api_router.include_router(instruction.router, prefix="/instruction", tags=["instruction"])
api_router.include_router(test.router, prefix="/test", tags=["tests"])
