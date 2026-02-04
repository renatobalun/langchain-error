# app/ai/graph.py
import json
from typing import TypedDict, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from ai.models import ErrorAnalysis
from ai.models import ErrorSolution
import os
from dotenv import load_dotenv

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, api_key=OPENAI_API_KEY)

def analyze_error_node(error):
    system_message = SystemMessage("You are an SRE/Backend incident analyst. Given a production error payload, produce a JSON analysis.")
    user_message = HumanMessage(content=
            "ERROR PAYLOAD:\n"
            f"{json.dumps(error, ensure_ascii=False, indent=2)}\n\n"
            "Return structured JSON with: probable_root_cause, impact_assessment, urgency, "
            "signals_used, immediate_actions, deeper_investigation, confidence.")
    conversation = [system_message, user_message]
    analyzer = llm.with_structured_output(ErrorAnalysis)
    
    print("AI START")
    result: ErrorAnalysis = analyzer.invoke(conversation, {
        "error": error
    })
    print("AI DONE")
    
    final_result = result.model_dump()
    return final_result


def generate_solution_node(error_analysis):
    system_message = SystemMessage(content=
    """
You are a senior SRE and backend engineer.

You are given a structured error_analysis produced by a previous AI step.
Your task is to generate a concrete, actionable remediation plan based strictly
on that analysis.

You MUST generate ALL of the following sections:

1) CODE FIXES
- Provide concrete Python code changes.
- Use copy-pasteable code blocks.
- Clearly state where the code belongs (file name + brief context).
- Prefer minimal, safe changes.
- If multiple fixes are possible, choose the safest production-ready one.

2) CONFIGURATION CHANGES
- List exact configuration or environment variable changes.
- Be explicit (key, value, reason).
- Include database, infrastructure, or service-level configs if relevant.

3) DEPLOYMENT STEPS
- Provide step-by-step deployment instructions.
- Assume a standard production environment (CI/CD, Docker, or manual deploy).
- Steps must be executable by an engineer without interpretation.

4) ROLLBACK PLAN
- Describe how to safely revert the changes.
- Include what signals to monitor to decide rollback.
- Rollback steps must be clear and ordered.

IMPORTANT RULES:
- Base your solution ONLY on the provided error_analysis.
- Do NOT invent unrelated systems or technologies.
- Do NOT give high-level advice without concrete actions.
- Do NOT explain basic concepts.
- Be precise, technical, and production-focused.
- Prefer safety and reversibility over aggressiveness.

OUTPUT FORMAT:
Return a single structured JSON object with the following keys exactly:
{
  "code_fixes": [
    {
      "file": "string",
      "description": "string",
      "code": "string"
    }
  ],
  "configuration_changes": [
    {
      "key": "string",
      "value": "string",
      "reason": "string"
    }
  ],
  "deployment_steps": ["string"],
  "rollback_plan": {
    "signals_to_monitor": ["string"],
    "steps": ["string"]
  }
}

Do not include any additional text outside the JSON.
""")
    user_message = HumanMessage(content="ERROR ANALYSIS:\n"
                                f"{json.dumps(error_analysis, ensure_ascii=False, indent=2)}\n\n"
                                "Return structured JSON with: code_fixes, configuration_changes, deployment_steps and rollback_plan.")
    solution_maker = llm.with_structured_output(ErrorSolution)
    conversation = [system_message, user_message]
    result : ErrorSolution = solution_maker.invoke(conversation, {"error_analysis": error_analysis})
    final_result = result.model_dump()
    return final_result
    
