import os
import shutil

# The base directory where all session folders are stored.
SESSIONS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sessions'))

def _get_safe_path(path: str, session_id: str) -> str:
    """Validates that a path is inside the specific session's workspace."""
    session_workspace = os.path.join(SESSIONS_DIR, session_id, 'workspace')
    
    if not os.path.isdir(session_workspace):
        raise FileNotFoundError(f"Workspace for session '{session_id}' not found.")

    requested_path = os.path.normpath(os.path.join(session_workspace, path))
    
    if not requested_path.startswith(session_workspace):
        raise PermissionError(f"Attempted to access file outside of the session workspace: {path}")
    
    return requested_path

def create_file(path: str, content: str = "", session_id: str = None):
    safe_path = _get_safe_path(path, session_id)
    os.makedirs(os.path.dirname(safe_path), exist_ok=True)
    with open(safe_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[{session_id}] File created: {path}")

# --- UPDATE ALL OTHER FUNCTIONS TO ACCEPT session_id ---

def create_folder(path: str, session_id: str = None):
    safe_path = _get_safe_path(path, session_id)
    os.makedirs(safe_path, exist_ok=True)
    print(f"[{session_id}] Folder created: {path}")

def add_content(path: str, content: str, session_id: str = None):
    safe_path = _get_safe_path(path, session_id)
    if not os.path.exists(safe_path):
        raise FileNotFoundError(f"File not found, cannot add content: {path}")
    with open(safe_path, 'a', encoding='utf-8') as f:
        f.write(content)
    print(f"[{session_id}] Content added to: {path}")

def delete_file(path: str, session_id: str = None):
    safe_path = _get_safe_path(path, session_id)
    if not os.path.isfile(safe_path):
        raise FileNotFoundError(f"File not found, cannot delete: {path}")
    os.remove(safe_path)
    print(f"[{session_id}] File deleted: {path}")

def delete_folder(path: str, session_id: str = None):
    safe_path = _get_safe_path(path, session_id)
    if not os.path.isdir(safe_path):
        raise FileNotFoundError(f"Folder not found, cannot delete: {path}")
    shutil.rmtree(safe_path)
    print(f"[{session_id}] Folder deleted: {path}")



def list_directory_contents(path: str, session_id: str) -> dict:
    """
    Lists the contents of a directory within the session's workspace.
    Returns a list of dictionaries, each representing a file or folder.
    """
    session_workspace = os.path.join(SESSIONS_DIR, session_id, 'workspace')
    full_path = os.path.join(session_workspace, path)

    if not os.path.isdir(full_path):
        return {"status": "error", "message": f"Path is not a directory: {path}"}

    contents = []
    for item in os.listdir(full_path):
        item_full_path = os.path.join(full_path, item)
        item_relative_path = os.path.join(path, item)
        if os.path.isdir(item_full_path):
            contents.append({"name": item, "type": "folder", "path": item_relative_path})
        else:
            contents.append({"name": item, "type": "file", "path": item_relative_path})
    return {"status": "success", "contents": contents}




def read_file_content(path: str, session_id: str) -> dict:
    """
    Reads the content of a file within the session's workspace.
    """
    session_workspace = os.path.join(SESSIONS_DIR, session_id, 'workspace')
    full_path = os.path.join(session_workspace, path)

    if not os.path.isfile(full_path):
        return {"status": "error", "message": f"File not found: {path}"}

    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return {"status": "success", "content": content}
    except Exception as e:
        return {"status": "error", "message": f"Failed to read file {path}: {e}"}

