from .msg import Msg, MsgUser, Interactive
from .msgtypes import MsgTypes


def format_message(msg) -> Msg | None:
    try:
        status = msg['entry'][0]['changes'][0]['value']['statuses'] if msg['entry'][0]['changes'][0]['value']['statuses'] else None
    except:
        status = None


    if status:
        return

    def find_message_type(msg):
        if msg['entry'][0]['changes'][0]['value']['messages'][0]['type'] == MsgTypes.text.name:
            return msg['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
        
        if msg['entry'][0]['changes'][0]['value']['messages'][0]['type'] == MsgTypes.interactive.name:
            return Interactive(
                id=msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name][msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name]['type']]['id'],
                title=msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name][msg['entry'][0]['changes'][0]['value']['messages'][0][MsgTypes.interactive.name]['type']]['title']
            )

    user = MsgUser(
        name=msg['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name'],
        number=msg['entry'][0]['changes'][0]['value']['contacts'][0]['wa_id']
    )

    new_msg = Msg(
        id=msg['entry'][0]['changes'][0]['value']['messages'][0]['id'],
        message=find_message_type(msg),  # type: ignore
        type=msg['entry'][0]['changes'][0]['value']['messages'][0]['type'],
        user=user
    )

    return new_msg