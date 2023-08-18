from pydantic import BaseModel

class Interactive(BaseModel):
    id: str
    title: str

class Image(BaseModel):
    mime_type: str
    id: str
    sha256: str

class MsgUser(BaseModel):
    number: str
    name: str

class Msg(BaseModel):
    id: str
    type: str
    message: str | Interactive | Image
    user: MsgUser

