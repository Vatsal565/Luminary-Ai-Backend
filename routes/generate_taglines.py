from fastapi import APIRouter
from pydantic import BaseModel
from services.generate_taglines import get_company_info
import dotenv
import config

dotenv.load_dotenv()
router = APIRouter()

class ChatRequest(BaseModel):
    company_description: str
    company_sector: str

@router.post("/tagline-generator")
async def tagline(request: ChatRequest):
    response = get_company_info(request.company_description, request.company_sector, config.GROQ_API_KEY)
    return {"response": response}