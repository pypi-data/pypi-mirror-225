from xia_fields import StringField, IntField
from xia_engine import Document


class Turn(Document):
    _key_fields = ["target", "mission", "dialog_id", "turn_id"]

    target: str = StringField(description="Target name of a campaign to change, like Project/Group")
    mission: str = StringField(description="Mission Name")
    dialog_id: str = StringField(description="Dialog ID")
    turn_id: int = IntField(description="Turn ID")
    author: str = StringField(description="Author of this turn")
    body: str = StringField(description="What is said", required=True)


class Dialog(Document):
    _key_fields = ["target", "mission", "dialog_id"]

    target: str = StringField(description="Target name of a campaign to change, like Project/Group")
    mission: str = StringField(description="Mission Name")
    dialog_id: str = StringField(description="Dialog ID")
    user: str = StringField(description="Author of Dialog")
    agent: str = StringField(description="Agent who makes responses")
