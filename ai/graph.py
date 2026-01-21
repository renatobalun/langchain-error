# app/ai/graph.py
from typing import TypedDict, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from ai.models import ErrorAnalysis

class State(TypedDict):
    error: Dict[str, Any]
    analysis: Dict[str, Any]

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an SRE/Backend incident analyst. "
     "Given a production error payload, produce a JSON analysis."),
    ("user",
     "ERROR PAYLOAD:\n{error}\n\n"
     "Return structured JSON with: probable_root_cause, impact_assessment, urgency, "
     "signals_used, immediate_actions, deeper_investigation, confidence.")
])

analyzer = prompt | llm.with_structured_output(ErrorAnalysis)

async def analyze_error_node(state: State) -> State:
    error = state["error"]
    print("AI START", state["error"].get("id"))
    result: ErrorAnalysis = await analyzer.ainvoke({
        "error": error
    })
    print("AI DONE", result.severity, result.urgency, result.confidence)
    state["analysis"] = result.model_dump()
    return state
