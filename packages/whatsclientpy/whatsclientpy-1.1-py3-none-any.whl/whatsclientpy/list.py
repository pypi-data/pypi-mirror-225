from .header import Header
from pydantic import BaseModel

class ListElement(BaseModel):
    execute: str
    title: str
    description: str | None = None

class SectionList(BaseModel):
    title: str
    rows: list[ListElement]

class List():
    def __init__(
        self,
        body: str,
        button: str,
        sections: list[SectionList],
        header: Header | None = None,
        footer: str | None = None,
    ) -> None:
        self.header = header
        self.body = body
        self.footer = footer
        self.button = button
        self.sections = sections
        pass

    def get(self, to: str):
        body = {
            'to': to,
            'type': 'interactive',
            'interactive': {
                'type': 'list',
                'body': {
                    'text': self.body
                },
                'action': {
                    'button': self.button,
                    'sections': [
                        {
                            'title': section.title,
                            'rows': [
                                {
                                    'id': row.execute.lower(),
                                    'title': row.title,
                                    'description': row.description
                                } for row in section.rows
                            ]
                        } for section in self.sections
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