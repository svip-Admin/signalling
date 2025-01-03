import websockets

"""
总的消息收发中心，将收到的消息分发给订阅的客户端
"""
class SignallingServer:
    peers: list = {}

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