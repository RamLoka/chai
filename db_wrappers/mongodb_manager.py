import os
from datetime import datetime, UTC
from typing import List, Dict, Optional
from pymongo import MongoClient
from pymongo.collection import Collection


class MongoDBManager:
    """
    Manages storing and retrieving chat conversations in MongoDB.
    Each conversation is stored as a single document with an array of messages.
    """

    def __init__(self, connection_string: str = "mongodb://localhost:27017/", database_name: str = "chai_db"):
        """
        Initializes the MongoDBManager.

        Args:
            connection_string (str): MongoDB connection string
            database_name (str): Name of the database to use
        """
        # --- TODO 1: Initialize MongoDB Connection ---
        # 1. Create a MongoClient using the connection_string
        # 2. Get the database using database_name
        # 3. Get the 'conversations' collection from the database
        # Store these as instance variables: self.client, self.db, self.conversations
        # Hint: self.client[database_name] gets a database
        # Hint: db[collection_name] gets a collection - use "conversations" as the collection_name
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.conversations = self.db["conversations"]

        self._ensure_indexes()

    def _ensure_indexes(self) -> None:
        """
        Creates indexes on the conversations collection for efficient querying.
        This is already implemented for you.
        """
        # Create a compound index on user_id and thread_name for fast lookups
        self.conversations.create_index([("user_id", 1), ("thread_name", 1)], unique=True)
        # Create an index on user_id for listing all threads for a user
        self.conversations.create_index("user_id")

    def get_conversation(self, user_id: str, thread_name: str) -> List[Dict]:
        """
        --- TODO 2: Retrieve a conversation from MongoDB ---
        """
        document = self.conversations.find_one({"user_id": user_id, "thread_name": thread_name})
        if not document or "messages" not in document:
            return []
        return document["messages"]

    def save_conversation(self, user_id: str, thread_name: str, messages: List[Dict]) -> None:
        """
        --- TODO 3: Save a conversation to MongoDB ---
        """
        conversation_id = f"{user_id}_{thread_name}"
        now = datetime.now(UTC).isoformat()
        document = {
            "_id": conversation_id,
            "user_id": user_id,
            "thread_name": thread_name,
            "messages": messages,
            "created_at": now,
            "updated_at": now
        }
        self.conversations.update_one(
            {"_id": conversation_id},
            {"$set": document},
            upsert=True
        )

    def append_message(self, user_id: str, thread_name: str, message: Dict) -> None:
        """
        --- TODO 4: Append a single message to a conversation ---
        """
        conversation_id = f"{user_id}_{thread_name}"
        message["timestamp"] = datetime.now(UTC).isoformat()
        update = {
            "$push": {"messages": message},
            "$set": {"updated_at": datetime.now(UTC).isoformat()},
            "$setOnInsert": {
                "_id": conversation_id,
                "user_id": user_id,
                "thread_name": thread_name,
                "created_at": datetime.now(UTC).isoformat()
            }
        }

        self.conversations.update_one(
            {"_id": conversation_id},
            update,
            upsert=True
        )

    def list_user_threads(self, user_id: str) -> List[str]:
        """
        --- TODO 5: List all conversation threads for a user ---
        """
        matches = list(self.conversations.find({"user_id": user_id}, {"thread_name": True, "_id": False}))
        thread_names = []
        for record in matches:
            thread_names.append(record["thread_name"])
        return thread_names

    def delete_conversation(self, user_id: str, thread_name: str) -> bool:
        """
        Deletes a conversation. Already implemented for you.

        Args:
            user_id (str): The user's ID
            thread_name (str): The name of the conversation thread

        Returns:
            bool: True if a conversation was deleted, False otherwise
        """
        conversation_id = f"{user_id}_{thread_name}"
        result = self.conversations.delete_one({"_id": conversation_id})
        return result.deleted_count > 0

    def close(self) -> None:
        """
        Closes the MongoDB connection. Already implemented for you.
        """
        if self.client:
            self.client.close()

    def _wipe_database(self) -> None:
        """
        **DANGEROUS**: Deletes all conversations. Only for testing!
        Already implemented for you.
        """
        self.conversations.delete_many({})


# Test code
if __name__ == "__main__":
    print("Testing MongoDBManager")

    # Update this connection string for your setup
    connection_string = "mongodb://localhost:27017/"
    # connection_string = "mongodb+srv://username:password@cluster.mongodb.net/"

    manager = MongoDBManager(connection_string=connection_string, database_name="chai_test_db")

    print("Testing MongoDBManager._ensure_indexes()")
    # Indexes are created automatically in __init__
    indexes = list(manager.conversations.list_indexes())
    print(f"Created {len(indexes)} indexes")

    print("\nTesting MongoDBManager.save_conversation()")
    messages = [
        {"role": "user", "content": "hello world"},
        {"role": "assistant", "content": "Hi there!"}
    ]
    manager.save_conversation("test_user", "test_thread", messages)
    print("Successfully saved conversation!")

    print("\nTesting MongoDBManager.get_conversation()")
    retrieved = manager.get_conversation("test_user", "test_thread")
    if len(retrieved) == 2:
        print("Successfully retrieved conversation!")
    else:
        print(f"Failed! Expected 2 messages, got {len(retrieved)}")

    print("\nTesting MongoDBManager.append_message()")
    manager.append_message("test_user", "test_thread", {"role": "user", "content": "another message"})
    retrieved = manager.get_conversation("test_user", "test_thread")
    if len(retrieved) == 3:
        print("Successfully appended message!")
    else:
        print(f"Failed! Expected 3 messages, got {len(retrieved)}")

    print("\nTesting MongoDBManager.list_user_threads()")
    manager.save_conversation("test_user", "thread2", [{"role": "user", "content": "test"}])
    threads = manager.list_user_threads("test_user")
    if len(threads) == 2:
        print(f"Successfully listed threads: {threads}")
    else:
        print(f"Failed! Expected 2 threads, got {len(threads)}: {threads}")

    print("\nCleaning up test data...")
    manager._wipe_database()
    manager.close()
    print("All tests passed!")
