from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from companies import get_company_info
from urllib.parse import unquote
from analysis import companies_analysis
from routes.chat_routes import router as chat_router
from dotenv import load_dotenv
import config
from routes.marketing_chatbot_routes import router as marketing_chatbot_router
from routes.generate_taglines import router as generate_taglines_router
from routes.seo_routes import router as seo_routes
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/home")
def read_root():
    return {
        'message': "Hello World!",
        'team': ['Vatsal', 'Miten', 'Laskhit']
    }

@app.get("/company")
def get_company_details(company: str, location: str):
    try:
        company = unquote(company)
        location = unquote(location)
        if config.GROQ_API_KEY is None:
            raise HTTPException(status_code=500, detail="API key is not set")
        company_info = get_company_info(company, location, api_key=config.GROQ_API_KEY)
        return company_info
    except Exception as e:
        return {
            "error": str(e)  # Return error message as JSON response if an exception occurs
        }

@app.post("/companies-analysis")
async def get_companies_analysis(request: Request):
    try:
        company_info = await request.json()
        if config.GROQ_API_KEY is None:
            raise HTTPException(status_code=500, detail="API key is not set")
        analysis_result = companies_analysis(company_info, api_key=config.GROQ_API_KEY)
        # print(analysis_result)
        return analysis_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

app.include_router(chat_router)
app.include_router(marketing_chatbot_router)
app.include_router(generate_taglines_router)
app.include_router(seo_routes)