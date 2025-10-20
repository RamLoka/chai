import os
import json
from typing import List

class FlatFileManager:
    """
    Manages storing and retrieving chat conversations in flat JSON files.
    """

    def __init__(self, storage_dir="data"):
        """
        Initializes the FlatFileManager for a specific user.
        """
        self.storage_dir = storage_dir
        self._ensure_storage_exists()
        self.conversations_index = {}  # Key: conversation_id => Value: Filepath
        self._init_index()

    def _ensure_storage_exists(self) -> None:
        """
        --- TODO 1: Create the storage directory ---
        """
        os.makedirs(self.storage_dir, exist_ok=True)

    def _init_index(self) -> None:
        """
        --- TODO 2: Load the conversations index file ---
        """
        index_file = os.path.join(self.storage_dir, "conversations.json")
        if not os.path.exists(index_file):
            self.conversations_index = {}
            self.save_index()
        else:
            with open(index_file, 'r') as f:
                self.conversations_index = json.load(f)

    def save_index(self) -> None:
        """
        --- TODO 3: Save the conversations index to disk ---
        """
        index_file = os.path.join(self.storage_dir, "conversations.json")
        with open(index_file, 'w') as f:
            json.dump(self.conversations_index, f, indent=2)

    def get_conversation(self, conversation_id: str) -> List[dict]:
        """
        --- TODO 4: Retrieve a user's conversation ---
        """
        if conversation_id not in self.conversations_index:
            return []

        filepath = os.path.join(self.storage_dir, self.conversations_index[conversation_id])
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def save_conversation(self, conversation_id: str, relative_filepath: str, messages: List[dict]) -> None:
        """
        --- TODO 5: Save a user's conversation ---
        """
        self.conversations_index[conversation_id] = relative_filepath
        self.save_index()

        filepath = os.path.join(self.storage_dir, relative_filepath)
        with open(filepath, 'w') as f:
            json.dump(messages, f, indent=2)

    def list_user_threads(self, user_id: str) -> List[str]:
        """
        List all conversation threads for a user.
        """
        threads = []
        prefix = f"{user_id}_"
        for conv_id in self.conversations_index.keys():
            if conv_id.startswith(prefix):
                threads.append(conv_id)
        return threads
