import argparse
import logging
import os
import socket
import asyncio

from server import SignallingServer

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s:%(lineno)s %(name)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


DEFAULT_RTC_CONFIG=""""{
    'lifetimeDuration':'86400s',
    'iceServers':[
    ],
    'blockStatus':'NOT_BLOCKED',
    'iceTransportPolicy':'all'
}"""



def rtc_config():
    pass

"""
程序启动入口
"""
def main():
    parser = argparse.ArgumentParser(description='signalling server setup params')
    # server args
    parser.add_argument('--host', type=str, default=os.environ.get('LISTEN_HOST', '0.0.0.0'),
                        help='Host to listen on for the signaling and web server, default: "0.0.0.0"')
    parser.add_argument('--port', type=int, default=os.environ.get('LISTEN_PORT', '8080'),
                        help='Port to listen on for the signaling and web server, default: "8080"')

    # authentication args
    parser.add_argument('--enable_basic_auth', default=os.environ.get('ENABLE_BASIC_AUTH', 'false'),
                        help='Enable Base authentication on server. Must set basic_auth_user and basic_auth_password to enforce Basic auth.')
    parser.add_argument('--basic_auth_user', default=os.environ.get('BASIC_AUTH_USER', ''),
                        help='Username for basic auth,default is to use the BASIC_AUTH_USER env var. Must also set basic_auth_password to enfore Basic auth.')
    parser.add_argument('--basic_auth_password', default=os.environ.get('BASIC_AUTH_PASSWORD', ''),
                        help='Password used when basic_auth_user is set.')
    # webserver args
    parser.add_argument('--enable_webserver', default=os.environ.get('ENABLE_WEBSERVER', 'false'),
                        help='Enable webserver, default is to use the ENABLE_WEBSERVER env var.')
    parser.add_argument('--web_root', default=os.environ.get('WEB_ROOT', '/opt/signalling-web'),
                        help='Root directory for webserver, default is to use the WEB_ROOT env var.')
    # coturn args
    parser.add_argument('--coturn_web_uri', default=os.environ.get('COTURN_WEB_URI', ''),
                        help='URI fro coturn REST API service, example: http://localhost:8081')
    parser.add_argument('--coturn_web_username',
                        default=os.environ.get('COTURN_WEB_USERNAME', f'vision-{socket.gethostname()}'),
                        help='URL for coturn REST API service, default is the system hostname.')
    parser.add_argument('--coturn_auth_header_name', default=os.environ.get('COTURN_AUTH_HEADER_NAME', 'x-auth-user'),
                        help='header name to pass user to coturn web service.')
    # rtc config args
    parser.add_argument('--rtc_config_json', default=os.environ.get('RTC_CONFIG_JSON', '/tmp/rtc.json'),
                        help='JSON file with RTC config to use as alternative to coturn service,read periodically.')

    # turn server args
    parser.add_argument('--turn_shared_secret', default=os.environ.get('TURN_SHARED_SECRET', ''),
                        help='shared TURN secret used to generate HMAC credentials,also requires TURN_HOST and TURN_PORT.')
    parser.add_argument('--turn_username', default=os.environ.get('TURN_USERNAME', ''),
                        help='Legacy non-HMAC TURN credential username,also requires TURN_HOST and TURN_PORT.')
    parser.add_argument('--turn_password', default=os.environ.get('TURN_PASSWORD', ''),
                        help='Legacy non-HMAC TURN credential password, also requires TURN_HOST and TURN_PORT.')
    parser.add_argument('--turn_host', default=os.environ.get('TURN_HOST', ''),
                        help='TURN host when generating RTC config from shared secret or legacy credentials.')
    parser.add_argument('--turn_port', default=os.environ.get('TURN_PORT', ''),
                        help='TURN port when generating RTC config from shared secret or legacy credentials.')
    parser.add_argument('--turn_protocol', default=os.environ.get('TURN_PROTOCOL', 'udp'),
                        help='TURN protocol for the client to use ("udp" or "tcp"), set to "tcp" without the quotes if "udp" is blocked on the network.')
    parser.add_argument('--turn_tls', default=os.environ.get('TURN_TLS', 'false'),
                        help='Enable or disable TURN over TLS (for the TCP protocol) or TURN over DTLS (for the UDP protocol), valid TURN server certificate required.')
    # app args
    parser.add_argument('--app_wait_ready', default=os.environ.get('APP_WAIT_READY', 'false'),
                        help='Waits for --app_ready_file to exist before starting stream if set to "true"')
    parser.add_argument('--app_ready_file', default=os.environ.get('APP_READY_FILE', '/tmp/appready'),
                        help='File set by sidecar used to indicate that app is initialized and ready')
    parser.add_argument('--streamer_port', default=os.environ.get('STREAMER_PORT', '8082'),
                        help='streamer port to recieve app streaming data"')
    parser.add_argument('--sfu_port', default=os.environ.get('SFU_PORT', '8889'),
                        help='sfu port to recieve player and streamer data')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging')
    parser.add_argument('--enable_ssl',default=os.environ.get('ENABLE_SSL','false'),
                        help='Enable SSL verification')
    parser.add_argument('--ssl_perm',default=os.environ.get('SSL_PERM',None),
                        help='perm file path')
    # 参数对象组装
    args = parser.parse_args()
    logger.warning(f'startup args: {args}')
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    using_basic_auth = args.enable_basic_auth
    using_turn_tls=args.turn_tls.lower() == 'true'
    turn_protocol = 'tcp' if args.turn_protocol.lower() == 'tcp' else 'udp'

    # 1.初始化信令服务所需的参数
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    options = argparse.Namespace()
    options.host = args.host
    options.port = args.port
    options.enable_basic_auth=args.enable_basic_auth
    options.basic_auth_user = args.basic_auth_user
    options.basic_auth_password = args.basic_auth_password
    options.enable_ssl = args.enable_ssl
    options.ssl_perm = args.ssl_perm
    options.health = "/health"
    options.enable_webserver=args.enable_webserver
    options.web_root=args.web_root
    options.keepalive_timeout=30
    options.rtc_config_file=args.rtc_config_json
    options.rtc_config=rtc_config
    options.turn_shared_secret=args.turn_shared_secret
    options.turn_host=args.turn_host
    options.turn_port=args.turn_port
    options.turn_protocol=turn_protocol
    options.turn_tls=using_turn_tls
    options.turn_auth_header_name=args.coturn_auth_header_name

    # 2.创建server
    server = SignallingServer(loop,options)


    # 启动服务
    try:
        asyncio.ensure_future(server.run(),loop=loop)
        asyncio.get_event_loop().run_forever()
    except:
        pass
    finally:
        # 关闭服务
        loop.run_until_complete(server.destroy())



if __name__ == '__main__':
    main()
