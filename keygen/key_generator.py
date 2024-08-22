import logging

import aiohttp
import random
import time
import uuid
import asyncio

from config import GamePromoTypes, GAME_PROMO_CONFIGS, GENERATE_INTERVAL, KEYGEN_THREAD_COUNT, KEYGEN_GAMES
from config import STARTUP_METHOD, StartupMethods

from common.database import db
from common.tools import get_timestamp

from aiohttp_socks import ProxyConnector


async def generate_client_id():
    timestamp = int(time.time() * 1000)
    random_numbers = ''.join([str(random.randint(0, 9)) for _ in range(19)])
    return f"{timestamp}-{random_numbers}"


async def login(session, client_id, game_data, proxy):
    url = 'https://api.gamepromo.io/promo/login-client'
    payload = {
        'appToken': game_data['appToken'],
        'clientId': client_id,
        'clientOrigin': 'deviceid'
    }
    async with session.post(url, json=payload, proxy=proxy) as response:
        data = await response.json()
        if response.status != 200:
            error_message = data.get('error_message', 'Failed to log in')
            raise Exception(error_message)
        return data['clientToken']


async def emulate_progress(session, client_token, game_data, proxy):
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
    async with session.post(url, json=payload, headers=headers, proxy=proxy) as response:
        data = await response.json()
        if response.status != 200:
            error_message = data.get('error_message', 'Failed to register event')
            raise Exception(error_message)
        return data['hasCode']


async def generate_key(session, client_token, game_data, proxy):
    url = 'https://api.gamepromo.io/promo/create-code'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {client_token}'
    }
    payload = {
        'promoId': game_data['promoId']
    }
    async with session.post(url, json=payload, headers=headers, proxy=proxy) as response:
        data = await response.json()
        if response.status != 200:
            error_message = data.get('error_message', 'Failed to generate key')
            raise Exception(error_message)
        return data['promoCode']


def sleep(seconds):
    return asyncio.sleep(seconds)


def delay_random():
    return random.random() / 3 + 1


async def generate_key_process(game_promo_type: GamePromoTypes, proxy=None):
    proxy_url = proxy
    logging.info(f"Key generation started. Game: {game_promo_type.value}. Proxy: {proxy_url}")

    if proxy:
        if proxy.startswith("socks"):
            connector = ProxyConnector.from_url(proxy, ssl=False)
            proxy = None  # in this case, the proxy server is transmitted in the session
        else:
            connector = aiohttp.TCPConnector(ssl=False)
    else:
        connector = None
    async with aiohttp.ClientSession(connector=connector) as session:
        while True:
            try:
                game_data = GAME_PROMO_CONFIGS[game_promo_type.value]
                client_id = await generate_client_id()
                client_token = await login(session, client_id, game_data, proxy)
                logging.info(f"[{get_timestamp()}] Logged in. Game: {game_promo_type.value}. Proxy: {proxy_url}")
                for _ in range(game_data['attemptsNumber']):
                    await sleep(game_data['eventsDelay'] * delay_random())
                    try:
                        has_code = await emulate_progress(session, client_token, game_data, proxy)
                    except Exception as e:
                        # logging.warn(f"Failed to emulate progress. Retrying. {e}, {game_promo_type.value}")
                        continue
                    if has_code:
                        break
                key = await generate_key(session, client_token, game_data, proxy)
                if len(key) < 1:
                    logging.warning(f"[{get_timestamp()}] Failed to get key for {game_promo_type.value}. Skipping. Proxy: {proxy_url}")
                    continue
                await db.keys_pool.insert_key(game_promo_type, key)
                logging.info(f"[{get_timestamp()}] New key generated: {game_promo_type.value}. Proxy: {proxy_url}")
            except Exception as e:
                logging.error(f"[{get_timestamp()}] Error generating key. Proxy: {proxy_url}: {e}")
            await sleep(GENERATE_INTERVAL)


def start_generating_keys(proxies):
    for game_type in KEYGEN_GAMES:
        for _ in range(KEYGEN_THREAD_COUNT):
            if proxies:
                for proxy in proxies:
                    asyncio.create_task(generate_key_process(game_type, proxy))
            else:
                asyncio.create_task(generate_key_process(game_type))


async def keygen_startup():
    try:
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        proxies = []
        logging.warning("Proxies file not found.")
    start_generating_keys(proxies)
    if STARTUP_METHOD is StartupMethods.OnlyKeygen:
        while True:
            await asyncio.sleep(3600)  # Main loop should keep running


