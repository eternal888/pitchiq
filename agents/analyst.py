from state import PitchState
from config import llm
from langchain_core.messages import HumanMessage

def analyst_agent(state: PitchState) -> PitchState:
    """
    Agent 2: Analyst — Production Grade
    Uses ALL researcher intelligence to score and map value props
    """

    contact_name = state["contact_name"]
    contact_title = state["contact_title"]
    hotel_name = state["hotel_name"]
    hotel_location = state.get("hotel_location", "")
    company_summary = state.get("company_summary", "")
    pain_points = state.get("pain_points", [])
    signals = state.get("signals", [])
    contact_summary = state.get("contact_summary", "")
    hotel_tier = state.get("hotel_tier", "")
    hiring_signals = state.get("hiring_signals", [])
    outreach_angle = state.get("outreach_angle", "")
    personalization_hook = state.get("personalization_hook", "")

    print(f"📊 Analysing {hotel_name}...")

    analysis = analyze_with_gemini(
        contact_name, contact_title, hotel_name, hotel_location,
        company_summary, pain_points, signals, contact_summary,
        hotel_tier, hiring_signals, outreach_angle, personalization_hook
    )

    print(f"✅ Analysis complete — Fit Score: {analysis['fit_score']}/100")
    print(f"   📌 Primary value prop angle: {analysis.get('primary_angle', 'general')}")

    return {
        **state,
        "fit_score": analysis["fit_score"],
        "value_props": analysis["value_props"]
    }


def analyze_with_gemini(
    contact_name, contact_title, hotel_name, hotel_location,
    summary, pain_points, signals, contact_summary,
    hotel_tier, hiring_signals, outreach_angle, personalization_hook
) -> dict:

    pain_str = "\n".join(pain_points) if pain_points else "Not identified"
    signal_str = "\n".join(signals) if signals else "Not identified"
    hiring_str = "\n".join(hiring_signals) if hiring_signals else "No hiring signals"

    prompt = f"""You are a senior B2B sales analyst for J.A. Uniforms, a premium uniform supplier for hotels.

Analyze this lead deeply and provide accurate scoring and value propositions.

=== HOTEL INTELLIGENCE ===
Hotel: {hotel_name} | {hotel_location}
Tier: {hotel_tier}
Summary: {summary}
Pain Points: {pain_str}
Buying Signals: {signal_str}
Hiring Signals: {hiring_str}
Outreach Angle: {outreach_angle}
Personalization Hook: {personalization_hook}

=== CONTACT INTELLIGENCE ===
Contact: {contact_name} — {contact_title}
Background: {contact_summary}

=== J.A. UNIFORMS OFFERINGS ===
- Custom uniforms tailored to brand standards
- Bulk ordering with volume discounts
- 48-hour delivery guarantee
- Inventory management portal
- Individual size profiles per employee
- Dedicated account manager

=== SCORING CRITERIA ===
Score 90-100: Luxury/upscale hotel, 200+ rooms, active hiring, renovation or expansion
Score 75-89: Upscale hotel, 100-200 rooms, stable operations
Score 50-74: Midscale hotel, moderate staff size
Score 25-49: Budget hotel, small staff
Score 0-24: Not hospitality related

=== YOUR TASK ===
Return in this exact format:
FIT_SCORE: [number 0-100]
PRIMARY_ANGLE: [the single best value prop angle based on outreach angle]
VALUE_PROPS: [value prop 1 tied to {outreach_angle}] | [value prop 2 tied to hiring/operations] | [value prop 3 tied to brand/quality]

Rules:
- Value props must be SPECIFIC to this hotel's situation
- Reference actual signals found (hiring numbers, renovation details)
- Each value prop must directly address {contact_title}'s priorities
- No generic statements — every prop must feel tailored
"""

    response = llm.invoke([HumanMessage(content=prompt)])
    return parse_response(response.content)


def parse_response(response: str) -> dict:
    lines = response.strip().split("\n")

    result = {"fit_score": 50, "value_props": [], "primary_angle": ""}

    for line in lines:
        if line.startswith("FIT_SCORE:"):
            try:
                result["fit_score"] = int(line.replace("FIT_SCORE:", "").strip())
            except:
                result["fit_score"] = 50
        elif line.startswith("PRIMARY_ANGLE:"):
            result["primary_angle"] = line.replace("PRIMARY_ANGLE:", "").strip()
        elif line.startswith("VALUE_PROPS:"):
            props = line.replace("VALUE_PROPS:", "").strip()
            result["value_props"] = [p.strip() for p in props.split("|")]

    return result