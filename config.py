import enum

GAME_PROMO_CONFIGS = {
    'MyCloneArmy': {
        'appToken': '74ee0b5b-775e-4bee-974f-63e7f4d5bacb',
        'promoId': 'fe693b26-b342-4159-8808-15e3ff7f8767'
    },
    'ChainCube2048': {
        'appToken': 'd1690a07-3780-4068-810f-9b5bbf2931b2',
        'promoId': 'b4170868-cef0-424f-8eb9-be0622e8e8e3'
    },
    'TrainMiner': {
        'appToken': '82647f43-3f87-402d-88dd-09a90025313f',
        'promoId': 'c4480ac7-e178-4973-8061-9ed5b2e17954'
    },
    'BikeRide3D': {
        'appToken': 'd28721be-fd2d-4b45-869e-9f253b554e50',
        'promoId': '43e35910-c168-4634-ad4f-52fd764a843f'
    }
}


class GamePromoTypes(enum.Enum):
    MyCloneArmy = 'MyCloneArmy'
    ChainCube2048 = 'ChainCube2048'
    TrainMiner = 'TrainMiner'
    BikeRide3D = 'BikeRide3D'


KEYGEN_ACTIVE = False
EVENTS_DELAY = 20
KEYGEN_THREAD_COUNT = 1
GENERATE_INTERVAL = 15

SUBSCRIBE_REQUIRED_CHANNEL_ID = -1002087798764
SUBSCRIBE_REQUIRED_CHANNEL_INVITE_LINK = "https://t.me/pdosi_project"

DEFAULT_DAILY_GAME_KEYS_LIMIT = 4

