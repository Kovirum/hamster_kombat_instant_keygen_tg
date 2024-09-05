from datetime import datetime
from datetime import timezone
from typing import Tuple, List

from pymongo import ReturnDocument

from config import GamePromoTypes, DEFAULT_DAILY_GAME_KEYS_LIMIT, DEFAULT_USER_MULTIPLIER, DEFAULT_LANGUAGE, \
    REQUEST_BROADCAST_CONFIRM, GAME_PROMO_CONFIGS


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
                    "last_used_date": current_date,
                    "history": {}
                }},
                return_document=ReturnDocument.AFTER
            )
        return user_doc

    async def set_user_language(self, user_id: int, lang_code: str):
        await self.init_user(user_id)
        await self.collection.update_one({"_id": user_id}, {"$set": {"language": lang_code}})

    async def get_user_language(self, user_id: int):
        user_doc = await self.init_user(user_id)
        return user_doc.get("language", DEFAULT_LANGUAGE)

    async def get_pool_limit(self, game: GamePromoTypes, user_id: int) -> Tuple[int, int]:
        """
        Calculates the remaining key limit and total available keys for a user in a specific game.

        Args:
            game (GamePromoTypes): The type of game for which the key limit is calculated.
            user_id (int): The user's identifier.

        Returns:
            Tuple[int, int]: A tuple where the first element is the remaining key limit,
                             and the second element is the total available keys.
        """
        user_doc = await self.init_user(user_id)
        game_data = GAME_PROMO_CONFIGS[game.value]
        user_game_limits = user_doc.get('limits', {}).get(game.value, {})
        user_game_limits_global = user_doc.get('limits', {}).get('global', {})
        game_keys_limit = user_game_limits.get('quanity') or user_game_limits_global.get('quanity') or game_data.get('game_gkey_limit') or DEFAULT_DAILY_GAME_KEYS_LIMIT
        game_keys_limit = int(game_keys_limit * (user_game_limits.get('multiplier') or user_game_limits_global.get('multiplier') or DEFAULT_USER_MULTIPLIER))
        already_used = len(user_doc['history'].get(game.value, []))

        remaining_limit = game_keys_limit - already_used
        total_available_keys = game_keys_limit

        return remaining_limit, total_available_keys

    async def count_key_receive(self, game: GamePromoTypes, user_id: int, keys: List[str]) -> None:
        user_doc = await self.init_user(user_id)
        user_history = user_doc['history']
        if game.value not in user_history:
            user_history[game.value] = []
        user_history[game.value].extend(keys)

        await self.collection.update_one(
            {"_id": user_id},
            {"$set": {"history": user_history}}
        )

    async def get_history_data(self, user_id: int) -> dict:
        user_doc = await self.init_user(user_id)
        return user_doc['history']

    async def get_users_for_broadcast(self):
        cursor = self.collection.find(
            {'broadcast': True} if REQUEST_BROADCAST_CONFIRM else {},
            {'_id': 1}
        )

        user_ids = [doc['_id'] for doc in await cursor.to_list(length=None)]
        return user_ids

    async def change_broadcast_subscribe_status(self, user_id: int) -> dict:
        """Changes the broadcast subscription status to the opposite and returns the modified document"""
        user_doc = await self.init_user(user_id)
        if not user_doc.get('broadcast'):
            user_doc['broadcast'] = True
        else:
            user_doc['broadcast'] = False
        await self.collection.update_one({"_id": user_id}, {"$set": {"broadcast": user_doc['broadcast']}})
        return user_doc
