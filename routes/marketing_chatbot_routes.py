from fastapi import APIRouter
from pydantic import BaseModel
from services.marketing_chatbot_service import get_chat_response

router = APIRouter()

class ChatRequest(BaseModel):
    msg: str

@router.post("/marketing-bot")
async def chat(request: ChatRequest):
    response = await get_chat_response(request.msg)
    return {"response": response}