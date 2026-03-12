from langgraph.graph import StateGraph, END
from state import PitchState
from researcher import researcher_agent
from analyst import analyst_agent
from writer import writer_agent
from critic import critic_agent
from scheduler import scheduler_agent

def should_rewrite(state: PitchState) -> str:
    """
    Conditional edge — decides what happens after Critic
    If approved → go to Scheduler
    If not approved → go back to Writer
    """
    if state.get("quality_approved"):
        return "scheduler"
    return "writer"


def build_graph():
    # Create the graph
    graph = StateGraph(PitchState)
    
    # Add all agents as nodes
    graph.add_node("researcher", researcher_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("scheduler", scheduler_agent)
    
    # Define the flow
    graph.set_entry_point("researcher")
    graph.add_edge("researcher", "analyst")
    graph.add_edge("analyst", "writer")
    graph.add_edge("writer", "critic")
    
    # Conditional edge after critic
    graph.add_conditional_edges(
        "critic",
        should_rewrite,
        {
            "writer": "writer",
            "scheduler": "scheduler"
        }
    )
    
    graph.add_edge("scheduler", END)
    
    return graph.compile()


# Run it
if __name__ == "__main__":
    pipeline = build_graph()
    
    result = pipeline.invoke({
        "company_name": "Marriott Hotels",
        "company_website": "https://example.com",
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
    
    print("\n" + "="*40)
    print("✅ LANGGRAPH PIPELINE COMPLETE")
    print("="*40)
    print(f"Company: {result['company_name']}")
    print(f"Fit Score: {result['fit_score']}/100")
    print(f"Email Subject: {result['email_subject']}")
    print(f"Quality Approved: {result['quality_approved']}")
    print(f"Send Time: {result['send_time']}")
    print(f"Follow Ups: {result['follow_up_sequence']}")