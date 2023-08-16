from xia_fields import StringField, JsonField
from xia_engine import Document


class Dialog(Document):
    target: str = StringField(description="Target name of a campaign to change, like Project/Group")
    mission: str = StringField(description="Mission Name")
    topic_id: str = StringField(description="Topic ID")
    topic: str = StringField(description="Topic content")
