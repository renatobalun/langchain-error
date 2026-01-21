This app is used for sending template errors.

default config:
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "http://localhost:8000/webhook/error")
ERROR_ROTATION_INTERVAL = int(os.getenv("ERROR_ROTATION_INTERVAL", "60"))  # seconds

startup:
1. add venv
2. install dependencies
3. run app: uvicorn main:app --port 8001 --reload

# Check error generator status
curl http://localhost:8001/

# Manually send current error to webhook
curl -X POST http://localhost:8001/send-error

# Get current error details
curl http://localhost:8001/current-error

# List all error types
curl http://localhost:8001/all-errors