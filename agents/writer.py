from state import PitchState

def writer_agent(state: PitchState) -> PitchState:
    """
    Agent 3: Writer
    Job: Generate a hyper-personalized email using
    everything the Researcher and Analyst found
    """
    
    company_name = state["company_name"]
    pain_points = state.get("pain_points", [])
    value_props = state.get("value_props", [])
    fit_score = state.get("fit_score", 0)
    
    print(f"✍️  Writing email for {company_name}...")
    
    # Only write if fit score is good enough
    if fit_score < 30:
        print(f"⚠️  Fit score too low ({fit_score}/100) — skipping")
        return {
            **state,
            "email_subject": None,
            "email_body": None
        }
    
    # Generate email
    subject = generate_subject(company_name, pain_points)
    body = generate_body(company_name, pain_points, value_props)
    
    print(f"✅ Email written successfully")
    
    return {
        **state,
        "email_subject": subject,
        "email_body": body
    }


def generate_subject(company_name: str, pain_points: list) -> str:
    """Generate a personalized subject line"""
    if pain_points:
        first_pain = pain_points[0].lower()
        return f"Quick idea for {company_name}'s {first_pain}"
    return f"Quick idea for {company_name}"


def generate_body(company_name: str, pain_points: list, value_props: list) -> str:
    """Generate personalized email body"""
    
    # Build pain point line
    pain_line = ""
    if pain_points:
        pain_line = f"I noticed {company_name} is likely dealing with {pain_points[0].lower()} — especially at your scale."
    
    # Build value prop line
    value_line = ""
    if value_props:
        value_line = value_props[0]
    
    email = f"""Hi [Name],

{pain_line}

We work with hotels and hospitality groups to solve exactly that. {value_line}

We recently helped a similar company cut their uniform procurement time by 60%.

Worth a 15-minute call to see if we can do the same for {company_name}?

Best,
Jay
J.A. Uniforms"""

    return email