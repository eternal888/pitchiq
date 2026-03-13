from state import PitchState
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

load_dotenv("../.env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def analyst_agent(state: PitchState) -> PitchState:
    """
    Agent 2: Analyst
    Job: Use Gemini to score the lead and map value props
    """
    
    company_name = state["company_name"]
    company_summary = state.get("company_summary", "")
    pain_points = state.get("pain_points", [])
    signals = state.get("signals", [])
    
    print(f"📊 Analysing {company_name}...")
    
    analysis = analyze_with_gemini(company_name, company_summary, pain_points, signals)
    
    print(f"✅ Analysis complete — Fit Score: {analysis['fit_score']}/100")
    
    return {
        **state,
        "fit_score": analysis["fit_score"],
        "value_props": analysis["value_props"]
    }


def analyze_with_gemini(company_name, summary, pain_points, signals) -> dict:
    
    pain_str = "\n".join(pain_points)
    signal_str = "\n".join(signals)
    
    prompt = f"""You are a B2B sales analyst for J.A. Uniforms, a premium uniform supplier for hotels.

Analyze this lead and provide scoring:

Company: {company_name}
Summary: {summary}
Pain Points: {pain_str}
Buying Signals: {signal_str}

J.A. Uniforms offers: custom uniforms, bulk ordering, 48-hour delivery, inventory management portal, size profiles per employee.

Return in this exact format:
FIT_SCORE: [number 0-100]
VALUE_PROPS: [specific value prop 1] | [specific value prop 2] | [specific value prop 3]

Score high (80-100) if: large hospitality company, multiple locations, staff uniformity matters
Score medium (50-79) if: smaller hotel, some uniform needs
Score low (0-49) if: not hospitality related
"""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    return parse_response(response.content)


def parse_response(response: str) -> dict:
    lines = response.strip().split("\n")
    
    result = {"fit_score": 50, "value_props": []}
    
    for line in lines:
        if line.startswith("FIT_SCORE:"):
            try:
                result["fit_score"] = int(line.replace("FIT_SCORE:", "").strip())
            except:
                result["fit_score"] = 50
        elif line.startswith("VALUE_PROPS:"):
            props = line.replace("VALUE_PROPS:", "").strip()
            result["value_props"] = [p.strip() for p in props.split("|")]
    
    return result