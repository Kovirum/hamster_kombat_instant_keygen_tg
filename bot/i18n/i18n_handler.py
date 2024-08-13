import os
from typing import List
import ujson
import aiofiles
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class I18nManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
            cls._instance.available_languages_data = []
        return cls._instance

    async def init(self) -> None:
        if not self.available_languages_data:
            try:
                for filename in self.get_available_language_paths():
                    file_path = os.path.join(os.path.dirname(__file__), 'locales', filename)
                    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                        data = ujson.loads(await f.read())
                        data['LANG_CODE'] = filename.split('.')[0]
                        self.available_languages_data.append(data)
                logger.info(f"Language data initialized. Total available languages: {len(self.available_languages_data)}")
            except Exception as e:
                logger.error(f"Error initializing language data: {e}")

    @staticmethod
    def get_available_language_paths() -> List[str]:
        paths = []
        locales_dir = os.path.join(os.path.dirname(__file__), 'locales')
        if not os.path.exists(locales_dir):
            logger.error(f"Locales directory does not exist: {locales_dir}")
            return paths
        try:
            paths = [f for f in os.listdir(locales_dir) if os.path.isfile(os.path.join(locales_dir, f))]
        except Exception as e:
            logger.error(f"Error listing locale directory: {e}")
        return paths

    @staticmethod
    async def get_translation(lang_code: str, key: str) -> str:
        file_path = os.path.join(os.path.dirname(__file__), 'locales', f'{lang_code}.json')
        if not os.path.exists(file_path):
            logger.error(f"Translation file not found: {file_path}")
            return key  # Return the key as fallback
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                data = ujson.loads(await f.read())
                return data.get(key, key)
        except Exception as e:
            logger.error(f"Error reading translation file {file_path}: {e}")
            return key  # Return the key as fallback
