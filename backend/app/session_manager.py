import os
import json
import uuid
from datetime import datetime

# Base directory for all sessions
SESSIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sessions'))
METADATA_FILE = os.path.join(SESSIONS_DIR, 'metadata.json')

def _read_metadata():
    """Reads the metadata file, creating it if it doesn't exist."""
    if not os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'w') as f:
            json.dump({}, f)
        return {}
    with open(METADATA_FILE, 'r') as f:
        return json.load(f)

def _write_metadata(data):
    """Writes data to the metadata file."""
    with open(METADATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def create_new_session():
    """Creates a new session and returns its details."""
    session_id = str(uuid.uuid4())
    session_path = os.path.join(SESSIONS_DIR, session_id)
    workspace_path = os.path.join(session_path, 'workspace')
    
    os.makedirs(workspace_path, exist_ok=True)
    
    # Create an empty history file
    open(os.path.join(session_path, 'history.jsonl'), 'w').close()

    metadata = _read_metadata()
    metadata[session_id] = {
        "id": session_id,
        "name": "New Chat", # A default name
        "created_at": datetime.utcnow().isoformat()
    }
    _write_metadata(metadata)
    
    print(f"Created new session: {session_id}")
    return metadata[session_id]

def get_all_sessions():
    """Returns a list of all sessions, sorted by creation date."""
    metadata = _read_metadata()
    sessions = list(metadata.values())
    # Sort sessions newest first
    sessions.sort(key=lambda s: s['created_at'], reverse=True)
    return sessions

def get_session_history(session_id: str):
    """Retrieves the chat history for a given session."""
    history_file = os.path.join(SESSIONS_DIR, session_id, 'history.jsonl')
    if not os.path.exists(history_file):
        return []
    
    history = []
    with open(history_file, 'r') as f:
        for line in f:
            history.append(json.loads(line))
    return history

def append_to_history(session_id: str, message_object: dict):
    """Appends a new message object to a session's history file."""
    history_file = os.path.join(SESSIONS_DIR, session_id, 'history.jsonl')
    # Ensure the message has a timestamp
    message_object['timestamp'] = datetime.utcnow().isoformat()
    with open(history_file, 'a') as f:
        f.write(json.dumps(message_object) + '\n')
