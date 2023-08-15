from xia_fields import StringField, DictField
from xia_engine import Document
from xia_gpt_prompts.knowledge import KnowledgeMap


class Campaign(Document):
    target: str = StringField(description="Target name of a campaign to change, like Project/Group")
    name: str = StringField(description="Campaign Name")
    scope_type: str = StringField(description="Type of scope", choices=["project", "group"], default="project")
    description = StringField(description="Campaign description")
    context_map: dict = DictField(description="Context Map for the given Campaign", default={})
