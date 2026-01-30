# main.py
from fastapi import FastAPI
from datetime import datetime
import asyncio
from contextlib import asynccontextmanager
import httpx
from typing import Optional
import logging
from error_sending.config import WEBHOOK_URL, ERRORS, ERROR_ROTATION_INTERVAL

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Error Generator Service", version="1.0.0")

# Configuration
current_error_index = 0

async def send_error_to_webhook(error_data: dict):
    """Send error data to webhook endpoint"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                WEBHOOK_URL,
                json=error_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                logger.info(f"✅ Successfully sent error '{error_data['error_name']}' to webhook")
            else:
                logger.error(f"❌ Webhook returned status code: {response.status_code}")
                
            return response.status_code
            
    except httpx.RequestError as e:
        logger.error(f"❌ Failed to send error to webhook: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}")
        return None


def create_error_payload(error_index: int) -> dict:
    """Create error payload with current timestamp"""
    error = ERRORS[error_index]
    
    return {
        "error_id": f"err_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{error_index}",
        "timestamp": datetime.now().isoformat(),
        "error_name": error["name"],
        "status_code": error["status_code"],
        "detail": error["detail"],
        "severity": error["severity"],
        "context": error["context"],
        "metrics": error["metrics"],
        "suggested_checks": error["suggested_checks"]
    }


async def rotate_and_send_errors():
    """Background task that rotates and sends errors every minute"""
    global current_error_index
    
    # Send initial error immediately
    error_payload = create_error_payload(current_error_index)
    await send_error_to_webhook(error_payload)
    
    while True:
        await asyncio.sleep(ERROR_ROTATION_INTERVAL)
        
        # Rotate to next error
        current_error_index = (current_error_index + 1) % len(ERRORS)
        
        # Create and send error payload
        error_payload = create_error_payload(current_error_index)
        await send_error_to_webhook(error_payload)
        
        logger.info(f"🔄 Rotated to error: {ERRORS[current_error_index]['name']}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("=" * 60)
    logger.info("🚀 Error Generator Service Started")
    logger.info(f"📡 Webhook URL: {WEBHOOK_URL}")
    logger.info(f"🔢 Total Error Types: {len(ERRORS)}")
    logger.info(f"⏱️  Rotation Interval: 60 seconds")
    logger.info(f"🎯 Initial Error: {ERRORS[current_error_index]['name']}")
    logger.info("=" * 60)
    
    # Start background task
    task = asyncio.create_task(rotate_and_send_errors())
    
    yield
    
    # Shutdown
    task.cancel()
    logger.info("🛑 Error Generator Service Stopped")


app = FastAPI(
    title="Error Generator Service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check and status endpoint"""
    return {
        "status": "running",
        "service": "Error Generator",
        "webhook_url": WEBHOOK_URL,
        "current_error": ERRORS[current_error_index]['name'],
        "total_error_types": len(ERRORS),
        "rotation_interval": "60 seconds",
        "endpoints": {
            "send_error": "POST /send-error - Manually trigger error send to webhook"
        }
    }


@app.post("/send-error")
async def send_error_immediately():
    """
    Manually trigger sending the current error to the webhook.
    This is a helper endpoint for testing without waiting for rotation.
    """
    error_payload = create_error_payload(current_error_index)
    
    logger.info(f"📤 Manual trigger: Sending error '{error_payload['error_name']}'")
    
    status_code = await send_error_to_webhook(error_payload)
    
    if status_code == 200:
        return {
            "success": True,
            "message": "Error sent successfully to webhook",
            "error_sent": error_payload['error_name'],
            "webhook_url": WEBHOOK_URL,
            "webhook_status": status_code
        }
    else:
        return {
            "success": False,
            "message": "Failed to send error to webhook",
            "error_name": error_payload['error_name'],
            "webhook_url": WEBHOOK_URL,
            "webhook_status": status_code
        }


@app.get("/current-error")
async def get_current_error():
    """Get the current error that will be sent"""
    return create_error_payload(current_error_index)


@app.get("/all-errors")
async def get_all_errors():
    """Get list of all error types"""
    return {
        "total": len(ERRORS),
        "errors": [
            {
                "index": i,
                "name": error["name"],
                "severity": error["severity"],
                "status_code": error["status_code"]
            }
            for i, error in enumerate(ERRORS)
        ]
    }