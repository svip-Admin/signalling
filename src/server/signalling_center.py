import base64
import functools
import hmac
import http
import json
import os
from enum import unique
from pathlib import Path

import websockets
from websockets.sync.server import basic_auth

from connections import PeerConnection
from constants import MIME_TYPES
from time import time
import hashlib
import utils

import logging

logger = logging.getLogger(__name__)


def generate_rtc_config(turn_host, turn_port, shared_secret, user, protocol='udp', turn_tls=False):
    user = user.replace(':', '-')

    # credential expires in 24hrs
    exp = int(time.time()) + 24 * 3600
    username = "{}-{}".format(exp, user)

    # Generate HMAC credential.
    key = bytes(shared_secret, 'ascii')
    raw = bytes(username, 'ascii')
    hashed = hmac.new(key, raw, hashlib.sha1())
    password = base64.b64encode(hashed.digest()).decode()

    rtc_config = {}
    rtc_config['lifetimeDuration'] = "{}s".format(24 * 3600)
    rtc_config['blockStatus'] = 'NOT_BLOCKED'
    rtc_config["iceTransportPolicy"] = "all"
    rtc_config["iceServers"] = []
    rtc_config["iceServers"].append({
        "urls": [
            "stun:{}:{}".format(turn_host, turn_port)
        ]
    })
    rtc_config["iceServers"].append({
        "urls": [
            "{}:{}:{}?transport={}".format('turns' if turn_tls else 'turn', turn_host, turn_port, protocol)
        ],
        "username": username,
        "credential": password
    })
    return json.dumps(rtc_config, indent=2)


"""
web服务以及websocket服务端
总的消息收发中心，将收到的消息分发给订阅的客户端
"""
class SignallingServer:
    # 存储browser、streaming、sfu的websocket
    peers: list

    def __init__(self, loop, options):
        logger.info('Initializing signalling server...')
        self.loop = loop
        self.options = options
        self.peers = {}
        self.loop = loop

        self.enable_ssl = options.enable_ssl
        self.ssl_perm = options.ssl_perm

        self.enable_webserver = options.enable_webserver
        self.web_root = options.web_root
        self.server = None
        self.holder = None

        self.host = options.host
        self.port = options.port
        self.keepalive_timeout = options.keepalive_timeout

        self.health_path = options.health
        self.cert_mtime = -1
        self.http_cache = {}

        self.enable_basic_auth = str(options.enable_basic_auth).lower() == 'true'
        self.basic_auth_user = options.basic_auth_user
        self.basic_auth_password = options.basic_auth_password

        self.cache_ttl=60

        if self.enable_webserver:
            for f in Path(self.web_root).rglob('*.*'):
                self.cache_file(f)

        self.turn_shared_secret = options.turn_shared_secret
        self.turn_host = options.turn_host
        self.turn_port = options.turn_port
        self.turn_protocol = options.turn_protocol.lower()
        if self.turn_protocol != 'tcp':
            self.turn_protocol = 'udp'
        self.turn_tls = options.turn_tls
        self.turn_auth_header_name=options.turn_auth_header_name

        self.rtc_config = options.rtc_config
        if os.path.exists(options.rtc_config_file):
            logger.info('{} parsing rtc_config_file: {}'.format(utils.get_format_time(),options.rtc_config_file))
            self.rtc_config = open(options.rtc_config_file, 'rb').read()
        if self.turn_shared_secret:
            if not (self.turn_host and self.turn_port):
                raise Exception('missing turn_host or turn_port options with turn_shared_secret')

        if self.enable_basic_auth:
            if not self.basic_auth_password:
                raise Exception('missing basic_auth_password when using enable_basic_auth option.')

    def set_rtc_config(self, rtc_config):
        self.rtc_config = rtc_config

    def cache_file(self, full_path):
        data, ttl = self.http_cache.get(full_path, (None, None))
        now = time()
        if data is None or now-ttl>self.cache_ttl:
            pass


    # 连接上来的客户端执行订阅
    def scribe(self, peer_connection: PeerConnection):
        self.peers[peer_connection.id] = peer_connection

    # 断开连接的客户端取消订阅
    def unscribe(self, id):
        self.peers.pop(id)

    # 向指定订阅者发布消息 点对点转发，在id没有的情况下 除了本身均会收到消息
    def publish(self, message, id=None):
        if hasattr(message, 'playerId'):
            self.peers

    async def request_process(self, server_root, connection, request):
        path = request.path
        headers = request.headers

        if self.enable_basic_auth:
            process_basic_auth = basic_auth(
                credentials=(self.basic_auth_user,self.basic_auth_password)
            )
            response = await process_basic_auth(connection,request)
            if response is not None:
                return response
        if path == '/ws' or path == '/ws/' or path.endswith('/signalling/') or path.endswith('/signalling'):
            return None
        if path == self.health_path:
            return connection.respond(http.HTTPStatus.OK,'OK\n')

        username = ''

        if path == '/turn/':
            if self.turn_shared_secret:
                if not username:
                    username= headers.get(self.turn_auth_header_name,"")





    async def response_process(self, connection, request, response):
        pass

    # 握手
    async def handshake(self, ws):
        raddr = ws.remote_addrss
        hello = await ws.recv()
        hello, unique_id = hello.split(maxsplit=1)
        if hello != 'HELLO':
            await ws.close(code=1002,reason='invalid protocol')
            raise Exception('Invalid hello from {!r}'.format(raddr))
        if not unique_id or unique_id in self.peers or unique_id.split()!=[unique_id]:
            await ws.close(code=1002,reason='invalid peer id')
            raise Exception('Invalid peer id {!r} from {!r}'.format(unique_id,raddr))
        await ws.send('HELLO')
        return unique_id

    async def connection_handler(self,ws,unique_id):
        pass

    """
    websocket/webserver的启动
    """
    async def run(self):
        async def handler(ws):
            raddr = ws.remote_address
            logger.info('Connected to {!r}'.format(raddr))
            unique_id = await self.handshake(ws)
            await self.connection_handler(ws,unique_id)
        http_handler = functools.partial(self.request_process,self.web_root)
        self.holder = await self.loop.create_future()
        with websockets.serve(handler,self.host,self.port,process_request=http_handler) as self.server:
            await self.holder

    """
    释放资源并关闭
    """

    async def destroy(self):
        pass
