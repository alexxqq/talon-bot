from pymongo import MongoClient
from config import MONGO_USER, MONGO_PASS, MONGO_HOST
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

URI = f'mongodb+srv://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}/?retryWrites=true&w=majority&appName=Users'

class MongoUserManager:
    client = MongoClient(URI)
    db = client.get_database('users')
    users_collection = db.get_collection('users')

    @classmethod
    def create_user(cls, user_id, username=None, cookies="", csrf_token="", question_type: str ="practic"):
        if cls.users_collection.find_one({"user_id": user_id}):
            return False

        user_data = {
            "user_id": user_id,
            "username": username,
            "cookies": cookies,
            "csrf_token": csrf_token,
            "question_type": question_type,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        result = cls.users_collection.insert_one(user_data)
        logger.info(f"User created with ID: {result.inserted_id}")
        return True

    @classmethod
    def update_user_field(cls, user_id: int, field_name: str, field_value: str | bool | int | list) -> bool:
        result = cls.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {field_name: field_value, "updated_at": datetime.utcnow()}}
        )

        return bool(result.matched_count)

    @classmethod
    def get_user(cls, user_id: int) -> dict:
        user = cls.users_collection.find_one({"user_id": user_id})
        return user

    @classmethod
    def delete_user(cls, user_id: int) -> bool:
        result = cls.users_collection.delete_one({"user_id": user_id})

        return bool(result.deleted_count)

    @classmethod
    def get_or_create_user(cls, user_id, username):
        user = cls.users_collection.find_one({"user_id": user_id})
        if not user:
            user_data = {
                "user_id": user_id,
                "username": username,
                "cookies": "",
                "csrf_token": "",
                "question_type": "practic",
                "offices_ids": [],
                "running": False,
                "created_at": datetime.utcnow(),
            }
            cls.users_collection.insert_one(user_data)
            return user_data
        return user

    @classmethod
    def set_running(cls, chat_id: int, running: bool) -> None:
        user = cls.users_collection.find_one({"user_id": chat_id})
        if not user:
            message = "User not found in the database. Please register using the bot."
            logger.info(message)
            return

        cls.users_collection.update_one({"user_id": chat_id}, {"$set": {"running": running}})
        
        status = "started" if running else "stopped"
        message = f"The script has been successfully {status}."
        logger.info(message)
    @classmethod
    def update_question_type(cls, user_id: int, question_type: str) -> bool:
        result = cls.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"question_type": question_type, "updated_at": datetime.utcnow()}}
        )

        return bool(result.matched_count)
    @classmethod
    def update_offices(cls, user_id: int, offices_ids: list) -> bool:
        result = cls.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"offices_ids": offices_ids, "updated_at": datetime.utcnow()}}
        )

        if result.matched_count:
            logger.info(f"Offices updated for user with ID {user_id}")
        else:
            logger.info(f"User with ID {user_id} not found")
        return bool(result.matched_count)
    @classmethod
    def update_credentials(cls, user_id: int, cookies: str, csrf_token: str) -> bool:
        result = cls.users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"cookies": cookies, "csrf_token": csrf_token, "updated_at": datetime.utcnow()}}
        )

        return bool(result.matched_count)
    @classmethod
    def get_running(cls, chat_id: int) -> bool:
        user = cls.users_collection.find_one({"user_id": chat_id})
        if not user:
            message = "User not found in the database. Please register using the bot."
            logger.info(message)
            return

        return user.get('running')