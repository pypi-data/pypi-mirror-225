import re
import ast
import json
from xia_engine import Document
from xia_fields import StringField


class KnowledgeNode(Document):
    _key_fields = ["target", "key"]

    target: str = StringField(description="Target name, like Project Name or Group Name")
    key: str = StringField(description="Knowledge Node Key, path separator is |")
    value: str = StringField(description="Knowledge Value")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._value_type, self._value_format = self.parse_format(self.value)

    @classmethod
    def parse_format(cls, value: str):
        if not value:
            return "text", "str"
        lines = [ln.strip() for ln in value.split("\n")]
        if lines[0].startswith("```"):
            if not lines[0][3:]:  # Case 1: Pure code with unknown code type
                return "code", "str"
            elif lines[0][3:] != "python":  # Case 2: Code with predefined code type
                return lines[0][3:], "str"
            if lines[1].startswith("["):  # Case 3: List in python code type
                return "python_encode", "list"
            if lines[1].startswith('"'):  # Case 4: String in python code type
                return "python_encode", "str"
            if lines[1].startswith("{"):  # Case 5: Dict in python code type
                return "python_encode", "dict"
            return "python", "str"
        return "text", "str"

    @classmethod
    def extract_code(cls, code_type: str, output_text: str):
        pattern = rf'```{code_type}.*?\s+(.*?)```'
        match = re.search(pattern, output_text, re.DOTALL)
        return match.group(1) if match else None

    @classmethod
    def extract_python_encode(cls, output_format: str, output_text: str):
        if output_format == "list":
            return cls.extract_list(output_text)
        else:
            return ast.literal_eval(output_text)

    @classmethod
    def extract_list(cls, output_text: str):
        pattern = r'\s*(.*=.*)?(\[.*\])'
        match = re.search(pattern, output_text, re.DOTALL)
        if match:
            tasks_list_str = match.group(2)
            list_value = ast.literal_eval(tasks_list_str)
        else:
            list_value = output_text.split("\n")
        return json.dumps(list_value, ensure_ascii=False)

    @classmethod
    def parse_output(cls, output_text: str, output_type: str, output_format: str):
        """Extract the related data from output text

        Args:
            output_format (str):
            output_type (str):
            output_text: Result of task

        Returns:
            Result if format is correct. None if format is not good
        """
        codes = ""
        if output_type != "text" or output_format != "str":
            code_type = "" if output_type == "code" else output_type
            code_type = "python" if output_type == "python_encode" else code_type
            codes = cls.extract_code(code_type, output_text)
        if output_type == "text" and output_format == "str":  # Simple text output
            return output_text
        if codes and output_type == "python_encode":  # Python encoded output
            return cls.extract_python_encode(output_format, codes)
        if codes and output_type != "text":  # Program code output
            return codes


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
