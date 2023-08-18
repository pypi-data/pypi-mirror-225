import requests
from .buttons import Buttons
from .list import List
import json

def send_controller(self, message: str | Buttons | List, to: str, message_id: str | None = None):
        body = {}
        if isinstance(message, str):
            body = {
                'to': to,
                'type': 'text',
                'text': {
                    'body': message,
                    'preview_url': 'true'
                },
                'recipient_type': 'individual',
                'messaging_product': 'whatsapp',
                'oa': 'true'
            }
        
        if isinstance(message, Buttons) or isinstance(message, List):
            body = message.get(to)

        if message_id:
            body['context'] = {
                'message_id': message_id
            }

        response = requests.post(
            url=f'https://graph.facebook.com/v16.0/{self.tel_id}/messages',
            data=json.dumps(body),
            headers={
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json',
                'accept': 'application/json'
            }
        )

        print(body)
        print(response.json())

        pass