from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
import uvicorn
import httpx
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="Simple FastAPI App",
    description="A simple FastAPI application with health endpoint and async calling endpoints",
    version="1.0.0"
)

# Global variable to track call history
call_history = []

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message"""
    return {"message": "Welcome to the Simple FastAPI App!"}

@app.get("/health")
async def health_check():
    """Health check endpoint that returns the application status"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Simple FastAPI App",
        "version": "1.0.0"
    }

async def delayed_call(url: str, delay_minutes: int = 5):
    """Background task that makes a delayed HTTP call"""
    try:
        await asyncio.sleep(delay_minutes * 60)  # Convert minutes to seconds
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            timestamp = datetime.utcnow().isoformat()
            call_history.append({
                "timestamp": timestamp,
                "url": url,
                "status_code": response.status_code,
                "response": response.json() if response.headers.get("content-type", "").startswith("application/json") else response.text
            })
            logger.info(f"Delayed call to {url} completed with status {response.status_code}")
    except Exception as e:
        timestamp = datetime.utcnow().isoformat()
        call_history.append({
            "timestamp": timestamp,
            "url": url,
            "error": str(e)
        })
        logger.error(f"Delayed call to {url} failed: {e}")

@app.get("/endpoint-a")
async def endpoint_a(background_tasks: BackgroundTasks):
    """Endpoint A that schedules a call to Endpoint B after 5 minutes"""
    endpoint_b_url = "https://system-test-sbqg.onrender.com/endpoint-b"
    
    # Schedule the delayed call to endpoint B
    background_tasks.add_task(delayed_call, endpoint_b_url)
    
    timestamp = datetime.utcnow().isoformat()
    logger.info(f"Endpoint A called at {timestamp}, scheduled call to Endpoint B in 5 minutes")
    
    return {
        "message": "Endpoint A called successfully",
        "timestamp": timestamp,
        "scheduled_call": f"Will call Endpoint B at {endpoint_b_url} in 5 minutes",
        "next_endpoint": "endpoint-b"
    }

@app.get("/endpoint-b")
async def endpoint_b(background_tasks: BackgroundTasks):
    """Endpoint B that schedules a call to Endpoint A after 5 minutes"""
    endpoint_a_url = "https://system-test-sbqg.onrender.com/endpoint-a"
    
    # Schedule the delayed call to endpoint A
    background_tasks.add_task(delayed_call, endpoint_a_url)
    
    timestamp = datetime.utcnow().isoformat()
    logger.info(f"Endpoint B called at {timestamp}, scheduled call to Endpoint A in 5 minutes")
    
    return {
        "message": "Endpoint B called successfully",
        "timestamp": timestamp,
        "scheduled_call": f"Will call Endpoint A at {endpoint_a_url} in 5 minutes",
        "next_endpoint": "endpoint-a"
    }

@app.get("/call-history")
async def get_call_history():
    """Get the history of all delayed calls made between endpoints"""
    return {
        "call_history": call_history,
        "total_calls": len(call_history),
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/start-cycle")
async def start_cycle(background_tasks: BackgroundTasks):
    """Start the calling cycle by calling Endpoint A"""
    endpoint_a_url = "https://system-test-sbqg.onrender.com/endpoint-a"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(endpoint_a_url)
            return {
                "message": "Cycle started successfully",
                "timestamp": datetime.utcnow().isoformat(),
                "initial_call_response": response.json()
            }
    except Exception as e:
        return {
            "message": "Failed to start cycle",
            "timestamp": datetime.utcnow().isoformat(),
            "error": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
