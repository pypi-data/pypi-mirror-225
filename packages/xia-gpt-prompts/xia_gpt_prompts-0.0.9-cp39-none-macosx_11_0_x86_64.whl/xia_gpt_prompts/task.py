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
from xia_gpt_prompts.knowledge import KnowledgeNode


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
                return KnowledgeNode.parse_output("\n".join(lines[1:]), self.output_type, self.output_format)


class Produce(Task):
    format: str = StringField("Example of Output format")
    guide: str = StringField("Guide to generate output ")

    """Points to be generated"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "format" not in kwargs:
            self.format = kwargs.get("format", self.get_block_content("format")).strip()
        if "guide" not in kwargs:
            self.guide = kwargs.get("guide", self.get_block_content("guide")).strip()
        self.output_type, self.output_format = KnowledgeNode.parse_format(self.format)
