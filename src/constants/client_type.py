from enum import IntEnum, Enum


class PlayerType(IntEnum):
    REGULAR = 0
    SFU = 1


class StreamerType(Enum):
    SFU_PEER_ID = 'SFU'
    LEGACY_PEER_ID = '__LEGACY__'


class IdType(Enum):
    SFU_PEER_ID = 'SFU'