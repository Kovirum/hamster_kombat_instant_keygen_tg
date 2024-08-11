from datetime import datetime
from datetime import timezone

from pymongo import ReturnDocument

from config import GamePromoTypes, DEFAULT_DAILY_GAME_KEYS_LIMIT


class DatabaseUsersData:
    def __init__(self, database, collection):
        self.database = database
        self.collection = collection

    async def init_user(self, user_id: int):
        """Creates a user document if it doesn't exist or returns the existing document.
           Also updates the 'last_used_date' field with the current date in 'dd.MM.yyyy' format."""
        try:
            current_date = datetime.now(timezone.utc).strftime("%d.%m.%Y")
            user_doc = await self.collection.find_one_and_update(
                {"_id": user_id},
                {
                    "$setOnInsert": {
                        "pools": {},
                        "last_used_date": current_date,
                        "history": {}}
                },
                upsert=True,
                return_document=ReturnDocument.AFTER
            )
            return await self.update_daily_limit(user_doc)
        except Exception as e:
            raise Exception(f"Failed to initialize user: {e}")

    async def update_daily_limit(self, user_doc: dict) -> dict:
        current_date = datetime.now(timezone.utc).strftime("%d.%m.%Y")
        if user_doc["last_used_date"] != current_date:
            user_doc = await self.collection.find_one_and_update(
                {"_id": user_doc["_id"]},
                {"$set": {
                    "pools": {},
                    "last_used_date": current_date,
                    "history": {}
                }},
                return_document=ReturnDocument.AFTER
            )
        return user_doc

    async def get_pool_limit(self, game: GamePromoTypes, user_id: int) -> int:
        user_doc = await self.init_user(user_id)
        game_keys_limit = user_doc.get('gkey_limit', DEFAULT_DAILY_GAME_KEYS_LIMIT)
        already_used = user_doc['pools'].get(game.value, 0)

        return game_keys_limit - already_used

    async def count_key_receive(self, game: GamePromoTypes, user_id: int, key: str) -> None:
        user_doc = await self.init_user(user_id)
        user_pools = user_doc['pools']
        user_history = user_doc['history']
        if game.value not in user_pools:
            user_pools[game.value] = 0
        if game.value not in user_history:
            user_history[game.value] = []
        user_pools[game.value] += 1
        user_history[game.value].append(key)

        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {
                "pools": user_pools,
                "history": user_history}}
        )

    async def get_history_data(self, user_id: int) -> dict:
        user_doc = await self.init_user(user_id)
        return user_doc['history']

    async def test(self) -> None:
        await self.collection.update_many(
            {"history": {"$exists": False}},
            {"$set": {"history": {}}}
        )
