import aiohttp
import random
import time
import uuid
import asyncio

from config import GamePromoTypes, GAME_PROMO_CONFIGS, EVENTS_DELAY, GENERATE_INTERVAL, KEYGEN_THREAD_COUNT

from common.database import db
from common.tools import get_timestamp


async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(19)])
    return f"{timestamp}-{random_numbers}"


async def login(session, client_id, game_data):
    url = 'https://api.gamepromo.io/promo/login-client'
    payload = {
        'appToken': game_data['appToken'],
        'clientId': client_id,
        'clientOrigin': 'deviceid'
    }
    async with session.post(url, json=payload) as response:
        data = await response.json()
        if response.status != 200:
            error_message = data.get('error_message', 'Failed to log in')
            raise Exception(error_message)
        return data['clientToken']


async def emulate_progress(session, client_token, game_data):
    url = 'https://api.gamepromo.io/promo/register-event'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_token}'
    }
    payload = {
        'promoId': game_data['promoId'],
        'eventId': str(uuid.uuid4()),
        'eventOrigin': 'undefined'
    }
    async with session.post(url, json=payload, headers=headers) as response:
        data = await response.json()
        if response.status != 200:
            error_message = data.get('error_message', 'Failed to register event')
            raise Exception(error_message)
        return data['hasCode']


async def generate_key(session, client_token, game_data):
    url = 'https://api.gamepromo.io/promo/create-code'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_token}'
    }
    payload = {
        'promoId': game_data['promoId']
    }
    async with session.post(url, json=payload, headers=headers) as response:
        data = await response.json()
        if response.status != 200:
            error_message = data.get('error_message', 'Failed to generate key')
            raise Exception(error_message)
        return data['promoCode']


def sleep(seconds):
    return asyncio.sleep(seconds)


def delay_random():
    return random.random() / 3 + 1


async def generate_key_process(game_promo_type: GamePromoTypes):
    print("Key generation started")
    while True:
        async with aiohttp.ClientSession() as session:
            try:
                game_data = GAME_PROMO_CONFIGS[game_promo_type.value]
                client_id = await generate_client_id()
                client_token = await login(session, client_id, game_data)
                print(f"[{get_timestamp()}] Logged in. Game: {game_promo_type.value}")
                for _ in range(10):
                    await sleep(EVENTS_DELAY * delay_random())
                    try:
                        has_code = await emulate_progress(session, client_token, game_data)
                    except Exception:
                        # logging.warn(f"Failed to emulate progress. Retrying. {e}, {game_promo_type.value}")
                        continue
                    if has_code:
                        break
                key = await generate_key(session, client_token, game_data)
                await db.keys_pool.insert_key(game_promo_type, key)
                print(f"[{get_timestamp()}] New key generated: {game_promo_type.value}")
            except Exception as e:
                print(f"[{get_timestamp()}] Error generating key: {e}")
        await sleep(GENERATE_INTERVAL)


def start_generating_keys():
    for game_type in GamePromoTypes:
        for _ in range(KEYGEN_THREAD_COUNT):
            asyncio.create_task(generate_key_process(game_type))


