This app is template for receiving errors app.
Use this code in your app for receiving errors.

startup:
1. add venv
2. install dependencies
3. run app: uvicorn webhook_receiver:app --port 8000 --reload

# Check webhook receiver
curl http://localhost:8000/

# View received errors
curl http://localhost:8000/errors

# View latest error
curl http://localhost:8000/errors/latest

# View error statistics
curl http://localhost:8000/errors/stats
