import enum

GAME_PROMO_CONFIGS = {
    'ChainCube2048': {
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3',
        'eventsDelay': 20,
        'attemptsNumber': 10,
    },
    'TrainMiner': {
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954',
        'eventsDelay': 20,
        'attemptsNumber': 10
    },
    'MergeAway': {
        'appToken': '8d1cc2ad-e097-4b86-90ef-7a27e19fb833',
        'promoId': 'dc128d28-c45b-411c-98ff-ac7726fbaea4',
        'eventsDelay': 20,
        'attemptsNumber': 10
    },
    'TwerkRace': {
        'appToken': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'promoId': '61308365-9d16-4040-8bb0-2f4a4c69074c',
        'eventsDelay': 20,
        'attemptsNumber': 10
    },
    'Polysphere': {
        'appToken': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'promoId': '2aaf5aee-2cbc-47ec-8a3f-0962cc14bc71',
        'eventsDelay': 20,
        'attemptsNumber': 20
    },
    'MowAndTrim': {
        'appToken': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'promoId': 'ef319a80-949a-492e-8ee0-424fb5fc20a6',
        'eventsDelay': 20,
        'attemptsNumber': 20
    },
    'Zoopolis': {
        'appToken': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'promoId': 'b2436c89-e0aa-4aed-8046-9b0515e1c46b',
        'eventsDelay': 21,
        'attemptsNumber': 23
    },
    'FluffCrusade': {
        'appToken': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'promoId': '112887b0-a8af-4eb2-ac63-d82df78283d9',
        'eventsDelay': 20,
        'attemptsNumber': 30,
        'game_gkey_limit': 8,
    },
    'TileTrio': {
        'appToken': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'promoId': 'e68b39d2-4880-4a31-b3aa-0393e7df10c7',
        'eventsDelay': 20,
        'attemptsNumber': 22
    },
    'StoneAge': {
        'appToken': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'promoId': '04ebd6de-69b7-43d1-9c4b-04a6ca3305af',
        'eventsDelay': 20,
        'attemptsNumber': 20
    },
    'Bouncemasters': {
        'appToken': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'promoId': 'bc72d3b9-8e91-4884-9c33-f72482f0db37',
        'eventsDelay': 20,
        'attemptsNumber': 30
    },
    'HideBall': {
        'appToken': "4bf4966c-4d22-439b-8ff2-dc5ebca1a600",
        'promoId': "4bf4966c-4d22-439b-8ff2-dc5ebca1a600",
        'eventsDelay': 30,
        'attemptsNumber': 20
    },
    'CountMasters': {
        'appToken': "4bdc17da-2601-449b-948e-f8c7bd376553",
        'promoId': "4bdc17da-2601-449b-948e-f8c7bd376553",
        'eventsDelay': 20,
        'attemptsNumber': 30
    },
    'PinOutMaster': {
        'appToken': 'd2378baf-d617-417a-9d99-d685824335f0',
        'promoId': 'd2378baf-d617-417a-9d99-d685824335f0',
        'eventsDelay': 20,
        'attemptsNumber': 30
    }
}

GamePromoTypes = enum.Enum('GamePromoTypes', {k: k for k in GAME_PROMO_CONFIGS.keys()})


class StartupMethods(enum.Enum):
    KeygenAndBot = 0
    OnlyKeygen = 1
    OnlyBot = 2


STARTUP_METHOD = StartupMethods.OnlyBot

KEYGEN_THREAD_COUNT = 1
KEYGEN_GAMES = [g for g in GamePromoTypes]
GENERATE_INTERVAL = 25

DEFAULT_LANGUAGE = 'en'  # it is required to specify one of the codes from the bot/i18n/locales directory
SUBSCRIBE_REQUIRED_CHANNEL_LIST = []  # If you have no idea what needs to be entered here, read the documentation

DEFAULT_DAILY_GAME_KEYS_LIMIT = 4
DEFAULT_USER_MULTIPLIER = 1.0
DEFAULT_NUM_KEYS_PER_REQUEST = 1

# YOU MUST KEEP THIS LINK OR OTHER MENTION OF AUTHORSHIP IN ORDER TO PRESERVE THE LICENSE
PROJECT_PDOSI_INVITE_URL = "https://t.me/pdosi_project"

ADMIN_ACCESS_IDS = []
REQUEST_BROADCAST_CONFIRM = True

