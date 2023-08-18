from enum import Enum

class MsgTypes(Enum):
    text = 'text',
    image = 'image',
    audio = 'audio',
    video = 'video',
    document = 'document',
    location = 'location',
    contact = 'contact',
    sticker = 'sticker',
    interactive = 'interactive'