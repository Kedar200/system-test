# Simple FastAPI App

A simple FastAPI application with a health check endpoint.

## Features

- Root endpoint (`/`) that returns a welcome message
- Health check endpoint (`/health`) that returns application status
- Two endpoints (`/endpoint-a` and `/endpoint-b`) that call each other with 5-minute delays
- Call history tracking (`/call-history`) to monitor delayed calls
- Cycle starter (`/start-cycle`) to initiate the calling loop
- Automatic API documentation with Swagger UI

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running the application
- **HTTPX**: Async HTTP client for making requests between endpoints

## Running the Application

### Option 1: Using Python directly
```bash
python main.py
```

### Option 2: Using Uvicorn command
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The application will be available at:
- Main app: http://localhost:8000
- Health check: http://localhost:8000/health
- Endpoint A: http://localhost:8000/endpoint-a
- Endpoint B: http://localhost:8000/endpoint-b
- Call history: http://localhost:8000/call-history
- Start cycle: http://localhost:8000/start-cycle
- API documentation: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### GET /
Returns a welcome message.

**Response:**
```json
{
  "message": "Welcome to the Simple FastAPI App!"
}
```

### GET /health
Returns the health status of the application.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000",
  "service": "Simple FastAPI App",
  "version": "1.0.0"
}
```

### GET /endpoint-a
Endpoint A that schedules a call to Endpoint B after 5 minutes.

**Response:**
```json
{
  "message": "Endpoint A called successfully",
  "timestamp": "2024-01-01T12:00:00.000000",
  "scheduled_call": "Will call Endpoint B at http://localhost:8000/endpoint-b in 5 minutes",
  "next_endpoint": "endpoint-b"
}
```

### GET /endpoint-b
Endpoint B that schedules a call to Endpoint A after 5 minutes.

**Response:**
```json
{
  "message": "Endpoint B called successfully",
  "timestamp": "2024-01-01T12:00:00.000000",
  "scheduled_call": "Will call Endpoint A at http://localhost:8000/endpoint-a in 5 minutes",
  "next_endpoint": "endpoint-a"
}
```

### GET /call-history
Returns the history of all delayed calls made between endpoints.

**Response:**
```json
{
  "call_history": [
    {
      "timestamp": "2024-01-01T12:05:00.000000",
      "url": "http://localhost:8000/endpoint-b",
      "status_code": 200,
      "response": {...}
    }
  ],
  "total_calls": 1,
  "timestamp": "2024-01-01T12:10:00.000000"
}
```

### GET /start-cycle
Starts the calling cycle by immediately calling Endpoint A, which will then schedule subsequent calls.

**Response:**
```json
{
  "message": "Cycle started successfully",
  "timestamp": "2024-01-01T12:00:00.000000",
  "initial_call_response": {...}
}
```

## How the Async Calling Works

1. **Call `/endpoint-a`**: This endpoint immediately returns a response and schedules a background task to call `/endpoint-b` after 5 minutes.

2. **Automatic Chain**: When `/endpoint-b` is called (after 5 minutes), it also schedules a call back to `/endpoint-a` after another 5 minutes.

3. **Continuous Loop**: This creates a continuous loop where the endpoints call each other every 5 minutes.

4. **Start the Cycle**: Use `/start-cycle` to begin the process, or manually call either endpoint.

5. **Monitor Activity**: Use `/call-history` to see all the delayed calls that have been made.

## Development

For development with auto-reload, use:
```bash
uvicorn main:app --reload
```

## Testing the Delayed Calls

1. Start the application
2. Call `/start-cycle` to begin the process
3. Monitor the logs to see when calls are scheduled and executed
4. Check `/call-history` to see the history of calls
5. For testing purposes, you can modify the delay from 5 minutes to a shorter duration in the code
