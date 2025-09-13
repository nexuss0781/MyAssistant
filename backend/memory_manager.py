import json
import os
from datetime import datetime
from typing import Dict, Any, List, Optional
import sqlite3
from pathlib import Path

class MemoryManager:
    def __init__(self, memory_dir: str = "memory"):
        """
        Initialize the memory manager with a directory for storing memory files.
        
        Args:
            memory_dir: Directory to store memory files
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Initialize SQLite database for structured memory
        self.db_path = self.memory_dir / "memory.db"
        self._init_database()
        
        # File paths for different types of memory
        self.knowledge_file = self.memory_dir / "knowledge.json"
        self.persona_file = self.memory_dir / "persona.json"
        self.preferences_file = self.memory_dir / "preferences.json"
        
        # Initialize files if they don't exist
        self._init_memory_files()
    
    def _init_database(self):
        """Initialize the SQLite database for memory storage."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create knowledge table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS knowledge (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    category TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    importance INTEGER DEFAULT 1
                )
            ''')
            
            # Create conversation history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    role TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Create user preferences table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_preferences (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
    
    def _init_memory_files(self):
        """Initialize memory files with default values if they don't exist."""
        if not self.knowledge_file.exists():
            self._save_json(self.knowledge_file, {})
        
        if not self.persona_file.exists():
            default_persona = {
                "personality_traits": ["helpful", "analytical", "creative"],
                "communication_style": "professional yet friendly",
                "expertise_areas": [],
                "learning_preferences": {},
                "last_updated": datetime.now().isoformat()
            }
            self._save_json(self.persona_file, default_persona)
        
        if not self.preferences_file.exists():
            self._save_json(self.preferences_file, {})
    
    def _save_json(self, file_path: Path, data: Dict[str, Any]):
        """Save data to a JSON file."""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load data from a JSON file."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_knowledge(self, key: str, value: Any, category: str = "general", importance: int = 1) -> bool:
        """
        Save knowledge to the memory system.
        
        Args:
            key: Unique identifier for the knowledge
            value: The knowledge content
            category: Category of knowledge (e.g., "user_info", "project", "general")
            importance: Importance level (1-10)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO knowledge (key, value, category, importance)
                    VALUES (?, ?, ?, ?)
                ''', (key, json.dumps(value), category, importance))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving knowledge: {e}")
            return False
    
    def retrieve_knowledge(self, key: str = None, category: str = None, limit: int = None) -> List[Dict[str, Any]]:
        """
        Retrieve knowledge from the memory system.
        
        Args:
            key: Specific key to retrieve (optional)
            category: Category to filter by (optional)
            limit: Maximum number of results (optional)
            
        Returns:
            List of knowledge entries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if key:
                    cursor.execute('SELECT * FROM knowledge WHERE key = ?', (key,))
                elif category:
                    query = 'SELECT * FROM knowledge WHERE category = ? ORDER BY importance DESC, timestamp DESC'
                    if limit:
                        query += f' LIMIT {limit}'
                    cursor.execute(query, (category,))
                else:
                    query = 'SELECT * FROM knowledge ORDER BY importance DESC, timestamp DESC'
                    if limit:
                        query += f' LIMIT {limit}'
                    cursor.execute(query)
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'id': row[0],
                        'key': row[1],
                        'value': json.loads(row[2]),
                        'category': row[3],
                        'timestamp': row[4],
                        'importance': row[5]
                    })
                
                return results
        except Exception as e:
            print(f"Error retrieving knowledge: {e}")
            return []
    
    def update_persona(self, updates: Dict[str, Any]) -> bool:
        """
        Update the AI persona with new information.
        
        Args:
            updates: Dictionary of persona updates
            
        Returns:
            True if successful, False otherwise
        """
        try:
            persona = self._load_json(self.persona_file)
            persona.update(updates)
            persona["last_updated"] = datetime.now().isoformat()
            self._save_json(self.persona_file, persona)
            return True
        except Exception as e:
            print(f"Error updating persona: {e}")
            return False
    
    def get_persona(self) -> Dict[str, Any]:
        """Get the current AI persona."""
        return self._load_json(self.persona_file)
    
    def save_conversation(self, session_id: str, message: str, role: str) -> bool:
        """
        Save a conversation message to memory.
        
        Args:
            session_id: Session identifier
            message: The message content
            role: Role of the message sender (user/assistant)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversation_history (session_id, message, role)
                    VALUES (?, ?, ?)
                ''', (session_id, message, role))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def get_conversation_history(self, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get conversation history for a session.
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of conversation messages
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM conversation_history 
                    WHERE session_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (session_id, limit))
                
                results = []
                for row in cursor.fetchall():
                    results.append({
                        'id': row[0],
                        'session_id': row[1],
                        'message': row[2],
                        'role': row[3],
                        'timestamp': row[4]
                    })
                
                return list(reversed(results))  # Return in chronological order
        except Exception as e:
            print(f"Error retrieving conversation history: {e}")
            return []
    
    def save_preference(self, key: str, value: Any) -> bool:
        """
        Save a user preference.
        
        Args:
            key: Preference key
            value: Preference value
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO user_preferences (key, value)
                    VALUES (?, ?)
                ''', (key, json.dumps(value)))
                conn.commit()
            return True
        except Exception as e:
            print(f"Error saving preference: {e}")
            return False
    
    def get_preference(self, key: str) -> Any:
        """
        Get a user preference.
        
        Args:
            key: Preference key
            
        Returns:
            Preference value or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT value FROM user_preferences WHERE key = ?', (key,))
                result = cursor.fetchone()
                return json.loads(result[0]) if result else None
        except Exception as e:
            print(f"Error retrieving preference: {e}")
            return None
    
    def clear_memory(self, memory_type: str = "all") -> bool:
        """
        Clear specific types of memory.
        
        Args:
            memory_type: Type of memory to clear ("knowledge", "conversations", "preferences", "all")
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                if memory_type == "knowledge" or memory_type == "all":
                    cursor.execute('DELETE FROM knowledge')
                
                if memory_type == "conversations" or memory_type == "all":
                    cursor.execute('DELETE FROM conversation_history')
                
                if memory_type == "preferences" or memory_type == "all":
                    cursor.execute('DELETE FROM user_preferences')
                
                conn.commit()
            
            if memory_type == "all":
                # Reset JSON files
                self._init_memory_files()
            
            return True
        except Exception as e:
            print(f"Error clearing memory: {e}")
            return False

# Example usage
if __name__ == "__main__":
    memory = MemoryManager()
    
    # Test knowledge storage
    memory.save_knowledge("user_name", "John Doe", "user_info", 5)
    memory.save_knowledge("project_type", "AI Assistant", "project", 3)
    
    # Test knowledge retrieval
    knowledge = memory.retrieve_knowledge(category="user_info")
    print("User info knowledge:", knowledge)
    
    # Test persona update
    memory.update_persona({"expertise_areas": ["AI", "Python", "Web Development"]})
    persona = memory.get_persona()
    print("Current persona:", persona)

