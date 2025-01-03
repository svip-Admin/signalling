from connections import PeerConnection
from constants.msg_type import MsgType
from event.message_event import MessageEvent
from proto.message import Offer, Answer, Config, PlayerDisconnected, IceCandidate, PlayerConnected, EndPointId, \
    EndpointIdConfirm, Identity


class StreamerConnection(PeerConnection):

    message_event = MessageEvent()

    @message_event.on(MsgType.OFFER.value)
    def offer(self,message: Offer,**kwargs):
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

    @message_event.on(MsgType.PLAYER_DISCONNECTED.value)
    def player_disconnected(self, message: PlayerDisconnected,**kwargs):
        pass

    @message_event.on(MsgType.PLAYER_CONNECTED.value)
    def player_connected(self, message: PlayerConnected,**kwargs):
        pass

    @message_event.on(MsgType.ENDPOINT_ID.value)
    def endpointId(self,message:EndPointId,**kwargs):
        pass

    @message_event.on(MsgType.ENDPOINT_ID_CONFIRM.value)
    def endpointIdConfirm(self,message:EndpointIdConfirm,**kwargs):
        pass

    @message_event.on(MsgType.IDENTIFY.value)
    def identify(self, message: Identity,**kwargs):
        pass