import websockets

from connections import PeerConnection

"""
总的消息收发中心，将收到的消息分发给订阅的客户端
服务只启动一次
"""
class SignallingServer:
    peers: list = {}

    # 连接上来的客户端执行订阅
    def scribe(self, peer_connection: PeerConnection):
        self.peers[peer_connection.id] = peer_connection

    # 断开连接的客户端取消订阅
    def unscribe(self, id):
        self.peers.pop(id)

    # 向订阅者发布消息
    def publish(self, message, id=None):
        if hasattr(message,'playerId'):
            self.peers
            pass


    """
    信令服务启动
    """
    async def run(self):
        async def handler(ws):
            pass

        with websockets.server(handler) as server:
            pass

    """
    释放资源并关闭
    """
    async def destroy(self):
        pass
