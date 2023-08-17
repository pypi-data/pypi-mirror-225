from xia_fields import StringField, DictField
from xia_engine import Document


class Campaign(Document):
    _key_fields = ["target", "name"]

    target: str = StringField(description="Target name of a campaign to change, like Project/Group")
    name: str = StringField(description="Campaign Name")
    owner: str = StringField(description="Mission Owner", required=True)
    scope_type: str = StringField(description="Type of scope", choices=["project", "group"], default="project")
    status: str = StringField(description="Campaign Status", default="opened", required=True,
                              choices=["opened", "closed"])
    description = StringField(description="Campaign description")

    def close(self):
        """Close the dialog"""
        self.update(status="closed")
