from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import json
import os

# Import the core modules
from .websocket_manager import ConnectionManager
from . import agent_core
from . import session_manager
from . import filesystem_tools # <-- NEW IMPORT

# This is the main FastAPI application instance
app = FastAPI(
    title="AI Agent Backend",
    description="The server-side logic for the autonomous AI agent.",
    version="1.0.0"
)

# CORS configuration
origins = [
    "http://localhost", "http://localhost:5173", "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# Single, shared instance of the ConnectionManager
manager = ConnectionManager()

# --- HEALTH CHECK ENDPOINT ---
@app.get("/health", tags=["Health Check"])
async def read_root():
    return {"status": "ok", "message": "AI Agent backend is running."}

# --- SESSION MANAGEMENT ENDPOINTS ---

@app.get("/sessions", tags=["Sessions"])
async def get_sessions():
    """Returns a list of all available sessions."""
    return session_manager.get_all_sessions()

@app.post("/sessions", tags=["Sessions"])
async def create_session():
    """Creates a new, empty session and returns its details."""
    new_session = session_manager.create_new_session()
    return new_session

@app.get("/sessions/{session_id}", tags=["Sessions"])
async def get_session(session_id: str):
    """Returns the complete message history for a given session."""
    history = session_manager.get_session_history(session_id)
    return history

# --- AGENT AND WEBSOCKET ENDPOINTS ---

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    finally:
        if client_id in manager.active_connections:
            manager.disconnect(client_id)


@app.post("/agent/run", tags=["Agent"])
async def run_agent(request: Request, background_tasks: BackgroundTasks):
    """
    (MODIFIED) Receives a prompt and SESSION_ID, then starts the agent's task.
    """
    try:
        data = await request.json()
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON body.")

    # --- MODIFIED VALIDATION ---
    user_prompt = data.get("user_prompt")
    session_id = data.get("session_id") # <-- NOW EXPECTS session_id
    client_id = data.get("client_id") # We still need this for the WebSocket

    if not all([user_prompt, session_id, client_id]):
        raise HTTPException(status_code=422, detail="Missing required fields: 'user_prompt', 'session_id', and 'client_id'.")

    # Pass the session_id to the background task
    background_tasks.add_task(
        agent_core.run_agent_task,
        user_prompt=user_prompt,
        session_id=session_id, # <-- PASSING SESSION_ID
        client_id=client_id,
        manager=manager
    )
    return {"status": "success", "message": "Agent task has been started for the specified session."}


# --- STATIC FILES ---
# Serve static files for unified Docker deployment
static_dir = "static"
if os.path.exists(static_dir):
    # Mount static assets (CSS, JS, etc.)
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")
    
    # Serve the React app for all non-API routes
    @app.get("/")
    async def serve_root():
        """Serve the main React application"""
        return FileResponse(f"{static_dir}/index.html")
    
    @app.get("/{catchall:path}")
    async def serve_frontend(catchall: str):
        """Serve React app for all frontend routes, API routes pass through"""
        # Let API routes pass through normally
        if (catchall.startswith("api/") or 
            catchall.startswith("ws/") or 
            catchall.startswith("sessions/") or 
            catchall.startswith("agent/") or
            catchall.startswith("health") or
            catchall.startswith("docs") or
            catchall.startswith("redoc") or
            catchall.startswith("openapi.json")):
            # This will cause a 404 for non-existent API routes
            raise HTTPException(status_code=404, detail="API endpoint not found")
        
        # For all other routes, serve the React app
        return FileResponse(f"{static_dir}/index.html")


@app.get("/sessions/{session_id}/files", tags=["Filesystem"])
async def get_session_files(session_id: str, path: str = "."):
    """Returns a list of files and folders within a session's workspace."""
    return filesystem_tools.list_directory_contents(path=path, session_id=session_id)



@app.get("/sessions/{session_id}/file_content", tags=["Filesystem"])
async def get_file_content(session_id: str, path: str):
    """Returns the content of a file within a session's workspace."""
    return filesystem_tools.read_file_content(path=path, session_id=session_id)


@app.post("/sessions/{session_id}/files", tags=["Filesystem"])
async def save_file_content(session_id: str, request: Request):
    """Saves content to a file within a session's workspace."""
    data = await request.json()
    path = data.get("path")
    content = data.get("content")

    if not path or content is None:
        raise HTTPException(status_code=422, detail="Missing 'path' or 'content' fields.")

    return await filesystem_tools.add_content(path=path, content=content, session_id=session_id)

