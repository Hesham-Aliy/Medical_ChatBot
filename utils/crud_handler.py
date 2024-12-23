from pymongo import MongoClient
from typing import List, Dict, Optional
from datetime import datetime


class MessageCrudHandler:
    def __init__(self, connection_string: str, database_name: str):
        """
        Initialize MongoDB connection and database.

        Parameters:
        connection_string (str): MongoDB connection string.
        database_name (str): Name of the database to connect to.
        """
        self.client = MongoClient(connection_string)
        self.db = self.client[database_name]
        self.conversations = self.db.conversations

    def create_conversation(self, conversation_id: str) -> str:
        """Create a new conversation with empty messages.

        This method initializes a new conversation document in the MongoDB collection
        with an empty messages array and timestamp fields.

        Args:
            conversation_id (str): Unique identifier for the conversation

        Returns:
            str: The ObjectId of the inserted conversation document as a string

        Example:
            >>> handler.create_conversation("12345")
            '507f1f77bcf86cd799439011'
        """
        conversation = {
            'conversation_id': conversation_id,
            'messages': [],
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        result = self.conversations.insert_one(conversation)
        return str(result.inserted_id)

    def add_message(self, conversation_id: str, nurse_message: str, bot_message: str) -> bool:
        """Add a new message pair to existing conversation.

        This method adds a nurse message and corresponding bot response to an existing conversation
        in the database. The conversation is identified by its unique conversation_id.

        Args:
            conversation_id (str): The unique identifier of the conversation.
            nurse_message (str): The message sent by the nurse.
            bot_message (str): The response generated by the bot.

        Returns:
            bool: True if the message pair was successfully added, False otherwise.

        Raises:
            ValueError: If the conversation_id does not exist in the database.

        Example:
            >>> crud.add_message("conv123", "How are you?", "I'm doing well, thanks!")
            True
        """
        if not self.get_conversation(conversation_id):
            raise ValueError(f"Conversation ID {conversation_id} not found.")
        message_pair = {
            'nurse': nurse_message,
            'bot': bot_message
        }
        result = self.conversations.update_one(
            {'conversation_id': conversation_id},
            {
                '$push': {'messages': message_pair},
                '$set': {'updated_at': datetime.now()}
            }
        )
        return result.modified_count > 0

    def get_conversation(self, conversation_id: str) -> Optional[Dict]:
        """Retrieve a conversation by its ID.

        Args:
            conversation_id (str): The unique identifier of the conversation to retrieve.

        Returns:
            Optional[Dict]: A dictionary containing the conversation data if found.

        Raises:
            ValueError: If no conversation is found with the given ID.

        Example:
            >>> crud_handler = CRUDHandler()
            >>> conversation = crud_handler.get_conversation("12345")
            >>> print(conversation)
            {'conversation_id': '12345', 'messages': [...]}
        """
        conversation = self.conversations.find_one(
            {'conversation_id': conversation_id})
        if not conversation:
            return None
        return conversation

    def get_messages(self, conversation_id: str) -> List[Dict]:
        """Get all messages from a conversation.

        This method retrieves all messages associated with a specific conversation ID.
        If the conversation exists, it returns the list of messages. If the conversation
        doesn't exist or has no messages, it returns an empty list.

        Args:
            conversation_id (str): The unique identifier of the conversation

        Returns:
            List[Dict]: A list of message dictionaries. Each dictionary contains message details.
            Returns empty list if conversation not found or has no messages.

        Example:
            >>> messages = crud_handler.get_messages("conv123")
            >>> print(messages)
            [{'message_id': '1', 'content': 'Hello'}, {'message_id': '2', 'content': 'Hi'}]
        """
        conversation = self.get_conversation(conversation_id)
        return conversation.get('messages', []) if conversation else []

    def delete_conversation(self, conversation_id: str) -> bool:
        """
        Delete a conversation by its ID. If the conversation does not exist, return False.

        Parameters:
        conversation_id (str): The ID of the conversation to delete.

        Returns:
        bool: True if the conversation was deleted, False otherwise.
        """
        if not self.get_conversation(conversation_id):
            raise ValueError(f"Conversation ID {conversation_id} not found.")
        result = self.conversations.delete_one(
            {'conversation_id': conversation_id})
        return result.deleted_count > 0

    def close_connection(self):
        """
        Close MongoDB connection.

        This method closes the connection to the MongoDB client, ensuring that all resources are properly released.
        """
        self.client.close()
