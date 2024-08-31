import logging
from typing import List

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

    async def get_keys(self, game: GamePromoTypes, count: int, limit: int) -> List[str] | None:
        """Retrieves and deletes the specified number of keys from the list of keys for the game."""
        key_count = min(count, limit)
        try:
            filter_query = {"_id": game.value, "keys.0": {"$exists": True}}
            game_doc = await self.collection.find_one_and_update(
                filter_query,
                [
                    {
                        '$set': {
                            'keys': {
                                '$cond': {
                                    'if': {'$gt': [{'$size': '$keys'}, key_count]},
                                    'then': {
                                        '$slice': ['$keys', key_count, {'$subtract': [{'$size': '$keys'}, key_count]}]
                                    },
                                    'else': []
                                }
                            }
                        }
                    }
                ],
                return_document=ReturnDocument.BEFORE
            )

            if game_doc and game_doc.get('keys'):
                return game_doc['keys'][:key_count]
            else:
                return None

        except Exception as e:
            logging.error(f"Failed to get keys: {e}")
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
