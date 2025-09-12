# MyAssistant/backend/app/memory_manager.py

import json
import os

MEMORY_DIR = "sessions"

def _get_memory_file_path(session_id: str) -> str:
    """Constructs the path to the memory file for a given session."""
    session_path = os.path.join(MEMORY_DIR, session_id)
    os.makedirs(session_path, exist_ok=True)
    return os.path.join(session_path, "memory.json")

def save_knowledge(session_id: str, key: str, value: any):
    """Saves a piece of knowledge (key-value pair) to the session's persistent memory."""
    memory_file = _get_memory_file_path(session_id)
    memory = {}
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory = json.load(f)
    
    memory[key] = value
    
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=4)
    print(f"[Memory Manager] Session {session_id}: Saved knowledge for key \'{key}\'")

def retrieve_knowledge(session_id: str, key: str, default: any = None) -> any:
    """Retrieves a piece of knowledge by its key from the session's persistent memory."""
    memory_file = _get_memory_file_path(session_id)
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory = json.load(f)
        print(f"[Memory Manager] Session {session_id}: Retrieved knowledge for key \'{key}\'")
        return memory.get(key, default)
    print(f"[Memory Manager] Session {session_id}: Knowledge for key \'{key}\' not found.")
    return default

def update_persona(session_id: str, persona_data: dict):
    """Updates the agent's persona data for a given session."""
    save_knowledge(session_id, "persona", persona_data)
    print(f"[Memory Manager] Session {session_id}: Updated agent persona.")

def get_all_memory(session_id: str) -> dict:
    """Retrieves all stored memory for a given session."""
    memory_file = _get_memory_file_path(session_id)
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            memory = json.load(f)
        return memory
    return {}

