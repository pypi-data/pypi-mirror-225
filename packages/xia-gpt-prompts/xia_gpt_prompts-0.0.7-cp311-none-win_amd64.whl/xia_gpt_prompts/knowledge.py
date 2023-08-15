from xia_engine import Document
from xia_fields import StringField


class KnowledgeNode(Document):
    _key_fields = ["target", "key"]

    target: str = StringField(description="Target name, like Project Name or Group Name")
    key: str = StringField(description="Knowledge Node Key, path separator is |")
    value_type: str = StringField(description="Value Type", default="text")
    value_format: str = StringField(description="Value Format", default="str")
    value: str = StringField(description="Knowledge Value")


class KnowledgeMap:
    def __init__(self, key: str, value: dict = None):
        self.key = key
        self.map = value if value else {}

    def add_node(self, node: KnowledgeNode):
        current_map = self.map
        for path in node.key.split("|"):
            if path not in current_map:
                current_map[path] = {}
            current_map = current_map[path]


class Goal:
    def __init__(self, name: str, brief: str):
        """The objective of a series mission

        Args:
            name: Goal Name
            brief: brief description of the goal
        """
        self.brief = brief
        self.knowledge_map = KnowledgeMap(key=name)
