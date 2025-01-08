from typing import Any
from connections import PeerConnection
from constants import msgtype
from event.message_event import MessageEvent
from proto import Offer, Answer, Config, IceCandidate, PlayerCount, Subscribe, UnSubscribe, ListStreamers, \
    StreamerList


class PlayerConnection(PeerConnection):
    subscribe: Any = None
    message_event = MessageEvent()

    @message_event.on(msgtype.OFFER.value)
    async def offer(self, message: Offer,**kwargs):
        pass

    @message_event.on(msgtype.ANSWER.value)
    async def answer(self, message: Answer,**kwargs):
        pass

    @message_event.on(msgtype.CONFIG.value)
    async def config(self, message: Config,**kwargs):
        pass

    @message_event.on(msgtype.ICE_CANDIDATE.value)
    async def ice_candidate(self, message: IceCandidate,**kwargs):
        pass

    @message_event.on(msgtype.PLAYER_COUNT.value)
    async def player_count(self, message: PlayerCount,**kwargs):
        pass

    @message_event.on(msgtype.SUBSCRIBE.value)
    async def subscribe(self, message: Subscribe,**kwargs):
        pass

    @message_event.on(msgtype.UNSUBSCRIBE.value)
    async def unsubscribe(self, message: UnSubscribe,**kwargs):
        pass

    @message_event.on(msgtype.LIST_STREAMERS.value)
    async def list_streamers(self,message:ListStreamers,**kwargs):
        pass

    @message_event.on(msgtype.STREAMER_LIST)
    async def streamer_list(self,message:StreamerList,**kwargs):
        pass



