from fastapi import APIRouter
from pydantic import BaseModel
from services.chat_service import get_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    msg: str

@router.post("/medical-bot")
async def chat(request: ChatRequest):
    response = await get_chat_response(request.msg)
    return {"response": response}