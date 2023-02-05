from fastapi import APIRouter

router = APIRouter()


@router.get("/categories")
async def categories():
    return {"hello": "world"}
