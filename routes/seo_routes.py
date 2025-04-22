from fastapi import APIRouter
from services.seo_service import get_seo

router = APIRouter()

@router.get("/seo")
async def fetch_company_info(company_description: str, location: str):
    """API to fetch company details"""
    return get_seo(company_description, location)