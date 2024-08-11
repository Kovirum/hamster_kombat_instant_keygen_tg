import logging
from pymongo import ReturnDocument

from config import GamePromoTypes


class DatabaseKeysPool:
    def __init__(self, database, collection):
        self.database = database
        self.collection = collection

    async def insert_key(self, game: GamePromoTypes, key: str) -> None:
        """Adds a key to the key pool for the game."""
        try:
            await self.collection.update_one(
                {"_id": game.value},
                {"$push": {"keys": key}},
                upsert=True
            )
        except Exception as e:
            logging.error(f"Failed to insert key: {e}")

    async def get_key(self, game: GamePromoTypes) -> str | None:
        """Retrieves and deletes the first key from the key pool for the game."""
        try:
            update_query = {"$pop": {"keys": -1}}
            game_doc = await self.collection.find_one_and_update(
                {"_id": game.value, "keys.0": {"$exists": True}},
                update_query,
                return_document=ReturnDocument.BEFORE
            )
            if game_doc and "keys" in game_doc and game_doc["keys"]:
                return game_doc["keys"][0]
            else:
                return None
        except Exception as e:
            logging.error(f"Failed to get key: {e}")
            return None

    async def count_key_pool(self, game: GamePromoTypes) -> int:
        """Returns the number of keys in the pool for the game."""
        try:
            pipeline = [
                {"$match": {"_id": game.value}},
                {"$project": {"_id": 0, "keysCount": {"$size": "$keys"}}}
            ]
            result = await self.collection.aggregate(pipeline).to_list(length=1)
            if result:
                return result[0]["keysCount"]
            return 0
        except Exception as e:
            logging.error(f"Failed to count key pool: {e}")
            return 0
