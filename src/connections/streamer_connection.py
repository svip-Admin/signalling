from connections import PeerConnection
from constants import msgtype
from event.message_event import MessageEvent
from proto import Offer, Answer, Config, PlayerDisconnected, IceCandidate, PlayerConnected, EndPointId, \
    EndpointIdConfirm, Identity


class StreamerConnection(PeerConnection):

    message_event = MessageEvent()

    @message_event.on(msgtype.OFFER.value)
    async def offer(self,message: Offer,**kwargs):
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

    @message_event.on(msgtype.PLAYER_DISCONNECTED.value)
    async def player_disconnected(self, message: PlayerDisconnected,**kwargs):
        pass

    @message_event.on(msgtype.PLAYER_CONNECTED.value)
    async def player_connected(self, message: PlayerConnected,**kwargs):
        pass

    @message_event.on(msgtype.ENDPOINT_ID.value)
    async def endpointId(self,message:EndPointId,**kwargs):
        pass

    @message_event.on(msgtype.ENDPOINT_ID_CONFIRM.value)
    async def endpointIdConfirm(self,message:EndpointIdConfirm,**kwargs):
        pass

    @message_event.on(msgtype.IDENTIFY.value)
    async def identify(self, message: Identity,**kwargs):
        pass
