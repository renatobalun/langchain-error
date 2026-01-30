# webhook_receiver.py
from fastapi import FastAPI, Request
from datetime import datetime
import logging
from ai.graph import analyze_error_node
from ai.graph import State


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Webhook Receiver", version="1.0.0")

# Store received errors
received_errors = []


@app.post("/webhook/error")
async def receive_error(request: Request):
    """
    Webhook endpoint that receives error data from the error generator service.
    This is where you would integrate your AI analysis logic.
    """
    try:
        error_data = await request.json()
        state : State = {"error":error_data, "analysis":{}}
        state = analyze_error_node(state)
        result = state["analysis"]
        # Add receipt timestamp
        error_data['received_at'] = datetime.now().isoformat()
        
        
        print("AI ANALYSIS")
        print("-"*20)
        print("ERROR ID:")
        print(result["error_id"])
        print()
        print("ERROR NAME:")
        print(result["error_name"])
        print()
        print("SEVERITY:")
        print(result["severity"])
        print()
        print("PROBABLE ROOT CAUSE:")
        print(result["probable_root_cause"])
        print()
        print("IMPACT ASSESMENT:")
        print(result["impact_assesment"])
        print()
        print("URGENCY:")
        print(result["urgency"])
        print()
        print("CONFIDENCE:")
        print(result["confidence"])
        print()
        print("SIGNALS USED:")
        for a in result["signals_used"]:
            print(a)
        print()
        print("IMMEDIATE ACTIONS:")
        for a in result["immediate_actions"]:
            print(a)
        print()
        print("DEEPER INVESTIGATION:")
        for a in result["deeper_investigation"]:
            print(a)
        print()
        print("ASSUMPTIONS:")
        for a in result["assumptions"]:
            print(a)
        print()
        
        
        
        # Store the error
        received_errors.append(error_data)
        
        # Keep only last 100 errors
        if len(received_errors) > 100:
            received_errors.pop(0)
        
        # Log the received error
        logger.info("=" * 60)
        logger.info(f"🚨 ERROR RECEIVED")
        logger.info(f"📛 Error Name: {error_data.get('error_name')}")
        logger.info(f"🆔 Error ID: {error_data.get('error_id')}")
        logger.info(f"⚠️  Severity: {error_data.get('severity')}")
        logger.info(f"📊 Status Code: {error_data.get('status_code')}")
        logger.info(f"📝 Detail: {error_data.get('detail')}")
        logger.info(f"🔧 Service: {error_data.get('context', {}).get('service')}")
        logger.info("=" * 60)
        
        # Here you would trigger your AI analysis
        # await analyze_error_with_ai(error_data)
        
        return {
            "status": "success",
            "message": "Error received and logged",
            "error_id": error_data.get('error_id'),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"❌ Failed to process webhook: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@app.get("/")
async def root():
    """Status endpoint"""
    return {
        "status": "running",
        "service": "Webhook Receiver",
        "total_errors_received": len(received_errors),
        "endpoints": {
            "webhook": "POST /webhook/error",
            "errors": "GET /errors",
            "latest": "GET /errors/latest"
        }
    }


@app.get("/errors")
async def get_all_errors(limit: int = 10):
    """Get all received errors"""
    return {
        "total": len(received_errors),
        "errors": received_errors[-limit:]
    }


@app.get("/errors/latest")
async def get_latest_error():
    """Get the most recent error"""
    if not received_errors:
        return {"message": "No errors received yet"}
    
    return received_errors[-1]


@app.get("/errors/stats")
async def get_error_statistics():
    """Get statistics about received errors"""
    if not received_errors:
        return {"message": "No errors received yet"}
    
    error_counts = {}
    severity_counts = {}
    
    for error in received_errors:
        # Count by error name
        name = error.get('error_name', 'Unknown')
        error_counts[name] = error_counts.get(name, 0) + 1
        
        # Count by severity
        severity = error.get('severity', 'Unknown')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    return {
        "total_errors": len(received_errors),
        "error_distribution": error_counts,
        "severity_distribution": severity_counts,
        "first_error": received_errors[0],
        "latest_error": received_errors[-1]
    }


@app.delete("/errors")
async def clear_errors():
    """Clear all received errors"""
    count = len(received_errors)
    received_errors.clear()
    return {
        "message": f"Cleared {count} errors",
        "remaining": len(received_errors)
    }