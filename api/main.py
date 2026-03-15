from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# So FastAPI can find the agents folder
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from graph import build_graph

app = FastAPI(title="PitchIQ API", version="1.0.0")

# Allow React frontend to connect later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchRequest(BaseModel):
    company_name: str
    company_website: str = ""

class ResearchResponse(BaseModel):
    company_name: str
    fit_score: int
    pain_points: list[str]
    value_props: list[str]
    email_subject: str
    email_body: str
    quality_approved: bool
    send_time: str
    follow_up_sequence: list[str]

@app.get("/")
def health_check():
    return {"status": "PitchIQ API is running 🚀"}

@app.post("/research", response_model=ResearchResponse)
def research_company(request: ResearchRequest):
    try:
        pipeline = build_graph()
        
        result = pipeline.invoke({
            "company_name": request.company_name,
            "company_website": request.company_website,
            "company_summary": None,
            "recent_news": None,
            "pain_points": None,
            "signals": None,
            "fit_score": None,
            "value_props": None,
            "email_subject": None,
            "email_body": None,
            "quality_approved": None,
            "quality_feedback": None,
            "send_time": None,
            "follow_up_sequence": None
        })
        
        return ResearchResponse(
            company_name=result["company_name"],
            fit_score=result["fit_score"] or 0,
            pain_points=result["pain_points"] or [],
            value_props=result["value_props"] or [],
            email_subject=result["email_subject"] or "",
            email_body=result["email_body"] or "",
            quality_approved=result["quality_approved"] or False,
            send_time=result["send_time"] or "",
            follow_up_sequence=result["follow_up_sequence"] or []
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))