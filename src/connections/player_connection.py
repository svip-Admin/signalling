from typing import Any
from connections import PeerConnection
from constants.msg_type import MsgType
from event.message_event import MessageEvent
from proto.message import Offer, Answer, Config, IceCandidate, PlayerCount, Subscribe, UnSubscribe, ListStreamers


class PlayerConnection(PeerConnection):
    subscribe: Any = None
    message_event = MessageEvent()

    @message_event.on(MsgType.OFFER.value)
    def offer(self, message: Offer,**kwargs):
        pass

    @message_event.on(MsgType.ANSWER.value)
    def answer(self, message: Answer,**kwargs):
        pass

    @message_event.on(MsgType.CONFIG.value)
    def config(self, message: Config,**kwargs):
        pass

    @message_event.on(MsgType.ICE_CANDIDATE.value)
    def ice_candidate(self, message: IceCandidate,**kwargs):
        pass

    @message_event.on(MsgType.PLAYER_COUNT.value)
    def player_count(self, message: PlayerCount,**kwargs):
        pass

    @message_event.on(MsgType.SUBSCRIBE.value)
    def subscribe(self, message: Subscribe,**kwargs):
        pass

    @message_event.on(MsgType.UNSUBSCRIBE.value)
    def unsubscribe(self, message: UnSubscribe,**kwargs):
        pass

    @message_event.on(MsgType.LIST_STREAMERS.value)
    def list_streamers(self,message:ListStreamers,**kwargs):
        pass


