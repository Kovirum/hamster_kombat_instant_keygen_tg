import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from .db_keys_pool import DatabaseKeysPool
from .db_users_data import DatabaseUsersData

import dns.resolver
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1']

load_dotenv()


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._client = AsyncIOMotorClient(os.getenv('DB_URL'))
        self._database = self._client.get_database("hamster_keygen_tg_db")
        self._keys_collection = self._database.get_collection("keys")
        self._users_collection = self._database.get_collection("users")

        self.keys_pool = DatabaseKeysPool(self._database, self._keys_collection)
        self.users_data = DatabaseUsersData(self._database, self._users_collection)

        logging.info("Database INITIALIZED")
