import logging
from typing import Dict, List

import json

from constants.client_type import StreamerType
from constants.msg_type import MsgType

logger = logging.getLogger(__name__)


class BaseMessage():
    type: str

    def __init__(self, type: str, **kwargs):
        self.type = type

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class Config(BaseMessage):

    def __init__(self, peerConnectionOptions: Dict = {}, protocolVersion: str = None, **kwargs):
        super().__init__(MsgType.CONFIG.value)
        self.peerConnectionOptions = peerConnectionOptions
        self.protocolVersion = protocolVersion

    @property
    def __dict__(self):
        _config = dict()
        _config['type'] = self.type
        _config['peerConnectionOptions'] = self.peerConnectionOptions
        if self.protocolVersion is not None:
            _config['protocolVersion'] = self.protocolVersion
        return _config


class Identity(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.IDENTIFY.value)


class EndPointId(BaseMessage):

    def __init__(self, id: str = StreamerType.LEGACY_PEER_ID.value, protocolVersion: str = None, **kwargs):
        super().__init__(MsgType.ENDPOINT_ID.value)
        self.id = id
        self.protocolVersion = protocolVersion

    @property
    def __dict__(self):
        _endpointId = dict()
        _endpointId['type'] = self.type
        _endpointId['id'] = self.id
        if self.protocolVersion is not None:
            _endpointId['protocolVersion'] = self.protocolVersion
        return _endpointId


class EndpointIdConfirm(BaseMessage):

    def __init__(self, committedId: str, **kwargs):
        super().__init__(MsgType.ENDPOINT_ID_CONFIRM.value)
        self.committedId = committedId


class StreamerIdChanged(BaseMessage):
    def __init__(self, newID: str, **kwargs):
        super().__init__(MsgType.STREAMER_ID_CHANGED.value)
        self.newID = newID


class ListStreamers(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.LIST_STREAMERS.value)


class StreamerList(BaseMessage):

    def __init__(self, ids: List[str], **kwargs):
        super().__init__(MsgType.LIST_STREAMERS.value)
        self.ids = ids


class Subscribe(BaseMessage):

    def __init__(self, streamerId: str, **kwargs):
        super().__init__(MsgType.SUBSCRIBE.value)
        self.streamerId = streamerId


class UnSubscribe(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.UNSUBSCRIBE.value)


class PlayerConnected(BaseMessage):
    def __init__(self, dataChannel: bool, sfu: bool, playerId: str, **kwargs):
        super().__init__(MsgType.PLAYER_CONNECTED.value)
        self.dataChannel = dataChannel
        self.sfu = sfu
        self.playerId = playerId


class PlayerDisconnected(BaseMessage):

    def __init__(self, playerId: str, **kwargs):
        super().__init__(MsgType.PLAYER_DISCONNECTED.value)
        self.playerId = playerId


class Offer(BaseMessage):

    def __init__(self, sdp: str, playerId: str = None, sfu: bool = None, multiplex: bool = None, **kwargs):
        super().__init__(MsgType.OFFER.value)
        self.sdp = sdp
        self.playerId = playerId
        self.sfu = sfu
        self.multiplex = multiplex

    @property
    def __dict__(self):
        _offer = dict()
        _offer['type'] = self.type
        _offer['sdp'] = self.sdp
        if self.playerId is not None:
            _offer['playerId'] = self.playerId
        if self.sfu is not None:
            _offer['sfu'] = self.sfu
        if self.multiplex is not None:
            _offer['multiplex'] = self.multiplex
        return _offer


class Answer(BaseMessage):
    def __init__(self, sdp: str, playerId: str = None, minBitrateBps: int = None, maxBitrateBps: int = None, **kwargs):
        super().__init__(MsgType.ANSWER.value)
        self.sdp = sdp
        self.playerId = playerId
        self.minBitrateBps = minBitrateBps
        self.maxBitrateBps = maxBitrateBps

        @property
        def __dict__(self):
            _answer = dict()
            _answer['type'] = self.type
            _answer['sdp'] = self.sdp
            if playerId is not None:
                _answer['playerId'] = self.playerId
            if self.minBitrateBps is not None:
                _answer['minBitrateBps'] = self.minBitrateBps
            if self.maxBitrateBps is not None:
                _answer['maxBitrateBps'] = self.maxBitrateBps
            return _answer


class IceCandidateData:

    def __init__(self, candidate: str, sdpMid: str, sdpMLineIndex: int, usernameFragment: str = None, **kwargs):
        self.candidate = candidate
        self.sdpMid = sdpMid
        self.sdpMLineIndex = sdpMLineIndex
        self.usernameFragment = usernameFragment

    @property
    def __dict__(self):
        _ice_candidateData = dict()
        _ice_candidateData['candidate'] = self.candidate
        _ice_candidateData['sdpMid'] = self.sdpMid
        _ice_candidateData['sdpMLineIndex'] = self.sdpMLineIndex
        if self.usernameFragment is not None:
            _ice_candidateData['usernameFragment'] = self.usernameFragment
        return _ice_candidateData


class IceCandidate(BaseMessage):
    candidate: IceCandidateData = None

    def __init__(self, candidate: IceCandidateData = None, playerId: str = None, **kwargs):
        super().__init__(MsgType.ICE_CANDIDATE.value)
        if candidate is not None:
            self.candidate = IceCandidateData(**candidate)
        self.playerId = playerId

    @property
    def __dict__(self):
        _ice = dict()
        _ice['type'] = self.type
        if self.candidate is not None:
            _ice['candidate'] = self.candidate.__dict__
        if self.playerId is not None:
            _ice['playerId'] = self.playerId
        return _ice


class DisconnectPlayer(BaseMessage):
    def __init__(self, playerId: str, reason: str = None, **kwargs):
        super().__init__(MsgType.DISCONNECT_PLAYER.value)
        self.playerId = playerId
        self.reason = reason

    @property
    def __dict__(self):
        _disconnect_player = dict()
        _disconnect_player['type'] = self.type
        _disconnect_player['playerId'] = self.playerId
        if self.reason:
            _disconnect_player['reason'] = self.reason
        return _disconnect_player


class Ping(BaseMessage):
    def __init__(self, time: int, **kwargs):
        super().__init__(MsgType.PING.value)
        self.time = time


class Pong(BaseMessage):
    def __init__(self, time: int, **kwargs):
        super().__init__(MsgType.PONG.value)
        self.time = time


class StreamerDisconnect(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.STREAMER_DISCONNECTED.value)


class LayerPreference(BaseMessage):
    def __init__(self, spatialLayer: int, temporalLayer: int, playerId: str, **kwargs):
        super().__init__(MsgType.LAYER_PREFERENCE.value)
        self.spatialLayer = spatialLayer
        self.temporalLayer = temporalLayer
        self.playerId = playerId


class DataChannelRequest(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.DATA_CHANNEL_REQUEST.value)


class PeerDataChannels(BaseMessage):

    def __init__(self, playerId: str, sendStreamId: int, recvStreamId: int, **kwargs):
        super().__init__(MsgType.PEER_DATA_CHANNELS.value)
        self.playerId = playerId
        self.sendStreamId = sendStreamId
        self.recvStreamId = recvStreamId


class PeerDataChannelsReady(BaseMessage):

    def __init__(self, **kwargs):
        super().__init__(MsgType.PEER_DATA_CHANNELS_READY.value)


class StreamerDataChannels(BaseMessage):
    def __init__(self, sfuId: str, sendStreamId: int, recvStreamId: int, **kwargs):
        super().__init__(MsgType.STREAMER_DATA_CHANNELS.value)
        self.sfuId = sfuId
        self.sendStreamId = sendStreamId
        self.recvStreamId = recvStreamId


class StartStreaming(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.START_STREAMING.value)


class StopStreaming(BaseMessage):
    def __init__(self, **kwargs):
        super().__init__(MsgType.STOP_STREAMING.value)


class PlayerCount(BaseMessage):
    def __init__(self, count: int, **kwargs):
        super().__init__(MsgType.PLAYER_COUNT.value)
        self.count = count


class Stats(BaseMessage):
    def __init__(self, data: str, **kwargs):
        super().__init__(MsgType.STATS.value)
        self.data = data


_generate_message_dict = {
    MsgType.CONFIG.value: Config,
    MsgType.IDENTIFY.value: Identity,
    MsgType.ENDPOINT_ID.value: EndPointId,
    MsgType.ENDPOINT_ID_CONFIRM.value: EndpointIdConfirm,
    MsgType.STREAMER_ID_CHANGED.value: StreamerIdChanged,
    MsgType.STREAMER_LIST.value: StreamerList,
    MsgType.SUBSCRIBE.value: Subscribe,
    MsgType.UNSUBSCRIBE.value: UnSubscribe,
    MsgType.PLAYER_CONNECTED.value: PlayerConnected,
    MsgType.PLAYER_DISCONNECTED.value: PlayerDisconnected,
    MsgType.OFFER.value: Offer,
    MsgType.ANSWER.value: Answer,
    MsgType.ICE_CANDIDATE.value: IceCandidate,
    MsgType.DISCONNECT_PLAYER.value: DisconnectPlayer,
    MsgType.PING.value: Ping,
    MsgType.PONG.value: Pong,
    MsgType.STREAMER_DISCONNECTED.value: StreamerDisconnect,
    MsgType.LAYER_PREFERENCE.value: LayerPreference,
    MsgType.DATA_CHANNEL_REQUEST.value: DataChannelRequest,
    MsgType.PEER_DATA_CHANNELS.value: PeerDataChannels,
    MsgType.PEER_DATA_CHANNELS_READY.value: PeerDataChannelsReady,
    MsgType.STREAMER_DATA_CHANNELS.value: StreamerDataChannels,
    MsgType.START_STREAMING.value: StartStreaming,
    MsgType.STOP_STREAMING.value: StopStreaming,
    MsgType.PLAYER_COUNT.value: PlayerCount,
    MsgType.STATS.value: Stats
}


def generate_from_message(msg):
    try:
        if isinstance(msg, str):
            msg = json.loads(msg)
    except Exception as e:
        logger.error(e)
    message = None
    message_type = msg['type']
    method = _generate_message_dict[message_type]
    if message_type is not None:
        message = method(**msg)
    return message


def generate_to_json(msg: Dict):
    return json.dumps(msg)


# ping = {"type":"ping","time":1721948820084}
#
# message = generate_from_message(ping)
# print(message.type)
# print(message.toJson())

