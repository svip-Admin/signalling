import json
import logging
from typing import Any

from proto.message import BaseMessage

logger = logging.getLogger(__name__)


class PeerConnection:
    id: str
    conn: Any = None

    async def send(self, message: BaseMessage=None,ws=None,**kwargs) -> bool:
        try:
            if message is None:
                logger.error("send message cannot be None")
                return False
            msg = json.dumps(message)
            if ws is not None and not ws.closed:
                await ws.send(msg)
            else:
                await self.conn.send(msg)
        except Exception as e:
            logger.error(f"send message has error: {e}")
            return False
        return True
