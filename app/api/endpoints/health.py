from fastapi import APIRouter
from fastapi_async_sqlalchemy import db
from sqlalchemy import text


router = APIRouter(
    prefix="/health",
    tags=["Health check"],
)


@router.get("/ping")
async def ping():
    return {"message": "pong"}


@router.get("/db")
async def check_db():
    await db.session.execute(text("SELECT VERSION()"))
    return {"message": "Success"}
