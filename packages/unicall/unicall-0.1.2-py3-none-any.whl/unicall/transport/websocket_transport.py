from .base_transport import Transport
from typing import *  # type: ignore

try:
    import websocket
except ImportError:
    websocket = None

try:
    import websockets
except ImportError:
    websockets = None

try:
    import wsproto
except ImportError:
    wsproto = None


class WebsocketTransport(Transport):
    def __init__(
        self,
        websocket: Union[
            "websocket.WebSocket",
            "websockets.WebSocketServerProtocol",
            "wsproto.Connection",
        ],
    ):
        # Exract the send/receive methods based on the type of websocket
        if websocket is not None and isinstance(websocket, websocket.WebSocket):
            send, receive = websocket.send, websocket.recv
        elif websockets is not None and isinstance(
            websocket, websockets.WebSocketServerProtocol
        ):
            send, receive = websocket.send, websocket.recv
        elif wsproto is not None and isinstance(websocket, wsproto.Connection):
            send, receive = websocket.send, websocket.receive
        else:
            raise ValueError(
                f"`websocket` must be a `websocket.WebSocket`, `websockets.WebSocketServerProtocol`, or `wsproto.Connection` instance, not {websocket!r}"
            )

        raise NotImplementedError("TODO")

    async def invoke(self, method: str, arguments: Dict[str, Any]) -> Any:
        raise NotImplementedError("TODO")

    async def receive(self) -> Tuple[str, Dict[str, Any]]:
        raise NotImplementedError("TODO")
