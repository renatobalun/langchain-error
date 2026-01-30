# app/ai/graph.py
import json
from typing import TypedDict, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ai.models import ErrorAnalysis
import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class State(TypedDict):
    error: Dict[str, Any]
    analysis: Dict[str, Any]

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)

def analyze_error_node(state: State) -> State:
    error = state["error"]
    
    system_message = SystemMessage("You are an SRE/Backend incident analyst. Given a production error payload, produce a JSON analysis.")
    user_message = HumanMessage(content=
            "ERROR PAYLOAD:\n"
            f"{json.dumps(error, ensure_ascii=False, indent=2)}\n\n"
            "Return structured JSON with: probable_root_cause, impact_assessment, urgency, "
            "signals_used, immediate_actions, deeper_investigation, confidence.")
    conversation = [system_message, user_message]
    analyzer = llm.with_structured_output(ErrorAnalysis)
    
    
    print("AI START", state["error"].get("error_id"))
    result: ErrorAnalysis = analyzer.invoke(conversation, {
        "error": error
    })
    print("AI DONE")
    state["analysis"] = result.model_dump()
    return state
