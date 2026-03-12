from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="AI Waste Nexus API")

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

STATE_FILE = "system_state.json"

@app.get("/status")
async def get_status():
    if not os.path.exists(STATE_FILE):
        return {
            "last_detected": {"category": "Waiting", "confidence": "0%", "timestamp": "00:00:00"},
            "stats": {"Plastic": 0, "Metal": 0, "Paper": 0, "Organic": 0},
            "history": []
        }
    
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading state: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "online", "hardware": "Raspberry Pi Gen 5"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
