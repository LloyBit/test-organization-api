''' Модуль для объединения всех роутов '''
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    """ Главная страница """
    return {"message": "Main page"}