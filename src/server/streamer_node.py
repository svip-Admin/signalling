from websockets import serve

class StreamerWebSocketServer:

    async def run(self):

        with serve() as self.server:
            pass