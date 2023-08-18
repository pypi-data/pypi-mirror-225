from .header_type import HeaderTypes

class Header():
    def __init__(
        self,
        type: HeaderTypes,
        text: str | None = None,
        url: str | None = None,
        preview_url: bool = True,
        filename: str | None = None,
    ) -> None:
        self.type = type
        self.text = text
        self.url = url
        self.preview_url = preview_url
        self.filename = filename
        pass

    def get(self):
        body = {
            'type': self.type.value
        }

        if self.type == HeaderTypes.text:
            body['text'] = self.text # type: ignore
            return body
        
        if self.type == HeaderTypes.image:
            body[self.type.value] = { # type: ignore
                'link': self.url
            }

            return body
        

        if self.type == HeaderTypes.document:
            body[self.type.value] = { # type: ignore
                'link': self.url,
                'filename': self.filename
            }

            if self.text:
                body[self.type.value]['caption'] = self.text # type: ignore

        return body