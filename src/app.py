import argparse
import logging
import os
from email.policy import default

logger = logging.getLogger(__name__)

"""
程序启动入口
"""


def main():
    parser = argparse.ArgumentParser(description='signalling server setup params')
    parser.add_argument('--host', '-h', type=str, default=os.environ.get('LISTEN_HOST', '0.0.0.0'),
                        help='Host to listen on for the signaling and web server, default: "0.0.0.0"')
    parser.add_argument('--port', '-p', type=int, default=os.environ.get('LISTEN_PORT', '8080'),
                        help='Port to listen on for the signaling and web server, default: "8080"')


if __name__ == '__main__':
    main()
