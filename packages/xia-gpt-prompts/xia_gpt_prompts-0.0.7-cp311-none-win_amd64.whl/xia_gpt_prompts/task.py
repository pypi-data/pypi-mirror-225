import json
import os
import sys
import re
import ast
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from jinja2.utils import concat
from xia_fields import StringField, JsonField
from xia_engine import EmbeddedDocument


class Task(EmbeddedDocument):
    _key_fields = ["name"]

    name: str = StringField(description="Task name")
    target: str = StringField(description="Target Knowledge Node Name")
    title: str = StringField(description="Task Title")
    output_type: str = StringField(description="Expected Output Type", default="text")
    output_format: str = StringField(description="Expected Output Format", default="str")
    sub_name: str = StringField(description="Task's secondary level name")
    required_contexts: list = JsonField(description="Json Field", default=[])

    @classmethod
    def get_jinja_env(cls, resource_type: str):
        package_dir = os.path.dirname(os.path.abspath(sys.modules[cls.__module__].__file__))
        task_template_dir = os.path.join(package_dir, "templates", resource_type)
        return Environment(
            loader=FileSystemLoader(searchpath=task_template_dir),
            trim_blocks=True,
            keep_trailing_newline=True
        )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.env = self.get_jinja_env("tasks")
        if "target" not in kwargs:
            self.target = self.name
        if "title" not in kwargs:
            self.title = ' '.join([word.capitalize() for word in self.name.split("_")])
            if self.sub_name:
                self.title = self.title + ': ' + self.sub_name

    def get_block_content(self, item_type: str, params: dict = None):
        params = {} if not params else params
        try:
            template = self.env.get_template(self.name + ".prompt")
        except TemplateNotFound:
            return ""
        context = template.new_context(params)
        if item_type not in template.blocks:
            return ""
        content = concat(template.blocks[item_type](context))
        return content

    def parse_output(self, output: str):
        pass


class Produce(Task):
    format: str = StringField("Example of Output format")
    guide: str = StringField("Guide to generate output ")

    @classmethod
    def parse_format(cls, value: str, default_type, default_format):
        if not value:
            return default_type, default_format
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
        return default_type, default_format

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

    def parse_output(self, output_text: str):
        """Extract the related data from output text

        Args:
            output_text: Output of GPT Engine

        Returns:
            Result if format is correct. None if format is not good
        """
        # Step 1: Get the content for the given produce task
        blocks = output_text.split("##")
        for block in blocks:
            lines = block.split("\n")
            if lines and self.title.lower() in lines[0].strip().lower():
                texts, codes = "", ""
                # Step 2: Get the correct output
                if self.output_type != "text" or self.output_format != str:
                    code_type = "" if self.output_type == "code" else self.output_type
                    code_type = "python" if self.output_type == "python_encode" else code_type
                    codes = self.extract_code(code_type, "\n".join(lines[1:]))
                # Step 3: Generating output
                if self.output_type == "text" and self.output_format == str:  # Simple text output
                    return "\n".join(lines[1:])
                if codes and self.output_type == "python_encode":  # Python encoded output
                    return self.extract_python_encode(self.output_format, codes)
                if codes and self.output_type != "text":  # Program code output
                    return codes

    """Points to be generated"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "format" not in kwargs:
            self.format = kwargs.get("format", self.get_block_content("format")).strip()
        if "guide" not in kwargs:
            self.guide = kwargs.get("guide", self.get_block_content("guide")).strip()
        self.output_type, self.output_format = self.parse_format(self.format, self.output_type, self.output_format)
