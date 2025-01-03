from enum import Enum


class MsgType(Enum):
    OFFER = 'offer'
    ANSWER = 'answer'
    ICE_CANDIDATE = 'iceCandidate'
    CONFIG = 'config'
    PLAYER_DISCONNECTED = 'playerDisconnected'
    PLAYER_COUNT = 'playerCount'
    SUBSCRIBE = 'subscribe'
    UNSUBSCRIBE = 'unsubscribe'
    STATS = 'stats'
    LIST_STREAMERS = 'listStreamers'
    STREAMER_LIST = 'streamerList'
    PLAYER_CONNECTED = 'playerConnected'

    DATA_CHANNEL_REQUEST = 'dataChannelRequest'
    PEER_DATA_CHANNELS_READY = 'peerDataChannelsReady'

    STREAMER_DATA_CHANNELS = 'streamerDataChannels'
    PEER_DATA_CHANNELS = 'peerDataChannels'
    STREAMER_DISCONNECTED = 'streamerDisconnected'

    ENDPOINT_ID = 'endpointId'
    IDENTIFY = 'identify'
    PING = 'ping'
    PONG = 'pong'
    DISCONNECT_PLAYER = 'disconnectPlayer'
    LAYER_PREFERENCE = 'layerPreference'
    REGISTER = 'register'
    SFU_SUBSCRIBE = 'sfu_subscribe'
    DISCONNECT_PEER = 'disconnectPeer'
    # 5.5 new add
    ENDPOINT_ID_CONFIRM = 'endpointIdConfirm'  # UE5.5中并未在解析类型中
    START_STREAMING = 'startStreaming'  # SFU发送给信令
    STOP_STREAMING = 'stopStreaming'  # SFU发送给信令
    STREAMER_ID_CHANGED = 'streamerIdChanged'
    UNKNOWN = 'unknown'

    @classmethod
    def parseFromMsgType(cls,msgType:str):
        for msg_type in MsgType:
            if msg_type.value == msgType:
                return msg_type
        return MsgType.UNKNOWN


msg_type = MsgType.parseFromMsgType("offer")
print(msg_type)