from socketio import Client as SocketClient
from .events import Events
from .msg import Msg
from typing import Callable
from .send import send_controller
from .on_message import format_message
from .buttons import Buttons
from .list import List
from .msg import Interactive


class Client():
    def __init__(
            self,
            token: str,
            socket: str,
            tel_id: str,
            responses: list[Callable[[Msg, 'Client'], None]] = []
    ):
        self.token = token
        self.socket = socket
        self.tel_id = tel_id
        self.responses = responses

        self.socket_client = SocketClient()
        pass

    def connect(self):
        def wrapped(func):
            self.socket_client.connect(self.socket)
            func('connected')
            self.socket_client.wait()
        return wrapped

    def send(self, message: str | Buttons | List, to: str, message_id: str | None = None):
        return send_controller(self, message, to, message_id)

    def on(self, event: Events):
        def wrapped(func: Callable[[Msg], None]):
            if event == Events.message:
                def on_message(msg):
                    message = format_message(msg)
                    if not message:
                        return
                    
                    if isinstance(message.message, Interactive):
                        for response in self.responses:
                            if response.__name__.lower() == message.message.id:
                                return response(message, self)

                    return func(message)

                self.socket_client.on('message', on_message)
            pass

        return wrapped
