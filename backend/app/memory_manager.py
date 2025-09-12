_# MyAssistant/backend/app/memory_manager.py

import json
import os
import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, session_id: str, memory_dir: str = "sessions"):
        self.session_id = session_id
        self.memory_dir = os.path.join(memory_dir, session_id)
        os.makedirs(self.memory_dir, exist_ok=True)
        self.knowledge_file = os.path.join(self.memory_dir, "knowledge.json")
        self.persona_file = os.path.join(self.memory_dir, "persona.json")

    async def _read_json_file(self, file_path: str, default_value: dict) -> dict:
        if not os.path.exists(file_path):
            return default_value
        try:
            async with asyncio.Lock(): # Ensure atomic file operations
                with open(file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Error decoding JSON from {file_path}: {e}")
            return default_value
        except Exception as e:
            logger.error(f"Error reading {file_path}: {e}")
            return default_value

    async def _write_json_file(self, file_path: str, data: dict):
        try:
            async with asyncio.Lock(): # Ensure atomic file operations
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
        except Exception as e:
            logger.error(f"Error writing to {file_path}: {e}")

    async def save_knowledge(self, key: str, value: any):
        """Saves a piece of knowledge to the session's persistent memory."""
        knowledge = await self._read_json_file(self.knowledge_file, {})
        knowledge[key] = value
        await self._write_json_file(self.knowledge_file, knowledge)
        logger.info(f"Knowledge saved: {key}")

    async def retrieve_knowledge(self, key: str, default: any = None) -> any:
        """Retrieves a piece of knowledge from the session's persistent memory."""
        knowledge = await self._read_json_file(self.knowledge_file, {})
        return knowledge.get(key, default)

    async def update_persona(self, persona_data: dict):
        """Updates the AI's persona with new attributes or preferences."""
        persona = await self._read_json_file(self.persona_file, {})
        persona.update(persona_data)
        await self._write_json_file(self.persona_file, persona)
        logger.info("Persona updated.")

    async def get_persona(self) -> dict:
        """Retrieves the current persona data."""
        return await self._read_json_file(self.persona_file, {})

    async def get_all_knowledge(self) -> dict:
        """Retrieves all stored knowledge for the session."""
        return await self._read_json_file(self.knowledge_file, {})

# Example usage (for testing purposes)
async def main():
    session_id = "test_session_123"
    memory_manager = MemoryManager(session_id)

    # Test saving and retrieving knowledge
    await memory_manager.save_knowledge("project_name", "Ethco AI")
    await memory_manager.save_knowledge("user_preference_theme", "dark")
    print(f"Project Name: {await memory_manager.retrieve_knowledge("project_name")}")
    print(f"User Theme: {await memory_manager.retrieve_knowledge("user_preference_theme")}")
    print(f"Non-existent key: {await memory_manager.retrieve_knowledge("non_existent", "default_value")}")

    # Test updating and getting persona
    await memory_manager.update_persona({"name": "Manus", "role": "AI Assistant"})
    await memory_manager.update_persona({"favorite_color": "blue"})
    print(f"Current Persona: {await memory_manager.get_persona()}")

    # Test getting all knowledge
    print(f"All Knowledge: {await memory_manager.get_all_knowledge()}")

    # Clean up test files
    # import shutil
    # shutil.rmtree(memory_manager.memory_dir)

if __name__ == "__main__":
    asyncio.run(main())
_
