from pydantic import BaseModel
from .header import Header

class Button(BaseModel):
    execute: str
    title: str


class Buttons():
    def __init__(
        self,
        body: str,
        buttons: list[Button],
        header: Header | None = None,
        footer: str | None = None,
    ) -> None:
        self.header = header
        self.body = body
        self.footer = footer
        self.buttons = buttons
        pass

    def get(self, to: str):
        body = {
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'button',
                'body': {
                    'text': self.body
                },
                'action': {
                    'buttons': [
                        {
                            'type': 'reply',
                            'reply': {
                                'id': button.execute.lower(),
                                'title': button.title
                            }
                        } for button in self.buttons
                    ]
                }

            },
            'recipient_type': 'individual',
            'messaging_product': 'whatsapp'
        }

        if self.header:
            body['interactive']['header'] = self.header.get()

        if self.footer:
            body['interactive']['footer'] = {
                'text': self.footer
            }

        return body