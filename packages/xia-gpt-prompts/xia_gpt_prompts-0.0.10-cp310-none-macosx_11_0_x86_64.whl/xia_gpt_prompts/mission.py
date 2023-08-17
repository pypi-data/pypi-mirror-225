import logging
import os
import sys
import uuid
import random
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from xia_gpt_prompts.task import Task, Produce
from xia_gpt_prompts.knowledge import KnowledgeNode
from xia_gpt_prompts.campaign import Campaign
from xia_gpt_prompts.dialog import Dialog, Turn
from xia_fields import StringField, JsonField
from xia_engine import Document, ListField, EmbeddedDocumentField, ExternalField


class Mission(Document):
    _key_fields = ["target", "campaign", "name"]

    target: str = StringField(description="Target name of a campaign to change, like Project/Group")
    campaign: str = StringField(description="Campaign Name")
    name: str = StringField(description="Mission Name")
    owner: str = StringField(description="Mission Owner", required=True)
    mission_type: str = StringField(description="Mission Type", required=True)
    status: str = StringField(description="Mission Status", default="opened", required=True,
                              choices=["opened", "closed"])
    profile: str = StringField(description="Requested Actor's profile", required=True)
    contexts: list = JsonField(description="Provided Context", default=[])
    tasks: list = ListField(EmbeddedDocumentField(document_type=Task), description="Tasks of the given mission",
                            default=[])
    campaign_details: Campaign = ExternalField(Campaign, field_map={"target": "target", "campaign": "name"},
                                               list_length=1)

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
        super(Mission, self).__init__(**kwargs)
        self.env = self.get_jinja_env("missions")

    def add_task(self, task: Task):
        self.contexts.extend(task.required_contexts)
        self.contexts = list(set(self.contexts))
        self.tasks.append(task)

    def get_context(self):
        context_list = []
        for context_key in self.contexts:
            context_content = KnowledgeNode.load(target=self.target, key=context_key)
            context_item = {
                "title": ' '.join([word.capitalize() for word in context_key.split("_")]),
                "content": context_content.value
            }
            context_list.append(context_item)
        return context_list

    def get_formats(self):
        formats = [{"title": task.title, "content": task.format} for task in self.tasks if task.format]
        return formats

    def get_guides(self):
        guides = [{"title": task.title, "content": task.guide} for task in self.tasks if task.guide]
        return guides

    def get_prompt(self, actor_role: str):
        """Get prompt for GPT call

        Args:
            actor_role: Description of action's profile

        Returns:
            prompts as string
        """
        try:
            template = self.env.get_template(self.mission_type + ".prompt")
        except TemplateNotFound:
            return None
        prompt = template.render(
            contexts=self.get_context(),
            formats=self.get_formats(),
            guides=self.get_guides(),
            actor_role=actor_role
        )
        return prompt

    def mission_validation(self):
        """Validate the mission"""
        return True

    def close(self):
        """Close the mission"""
        self.update(status="closed")

    async def run(self, actor):
        """Run the mission directly by an actor

        Process:
            * Mission is published
            * One or more actors apply for the mission
            * Get the response of actor
            * Response could be:
                * Standard response: Check if mission is completed => if OK job done
                * Need more context = Context to be added into mission
                * Not capable

        Args:
            actor: The actor to be used to execute the mission
        """
        # Step 1. Provide context
        request = self.get_prompt(self.profile)
        evaluation = actor.evaluate_mission(self.profile, request)
        if not evaluation:
            return  # Actor cannot finish the job, we could do nothing

        # Step 2. Actor accepts and will do the job
        contract = Dialog(target=self.target, mission=self.name, dialog_id=str(uuid.uuid4()),
                          user=self.owner, agent=actor.name).save()
        contract_id = contract.dialog_id
        Turn(target=self.target, mission=self.name, dialog_id=contract_id, turn_id=random.randint(1, 2**63),
             author=self.owner, body=request).save()
        response = await actor.execute_mission(self.profile, request)

        # Step 3. Validate the work / each type of task should have its validation
        if response["status"] != "successful":
            return  # Mission execution is not successful for this user

        result = response["result"]
        Turn(target=self.target, mission=self.name, dialog_id=contract_id, turn_id=random.randint(1, 2**63),
             author=actor.name, body=result).save()
        task_validation = {task.target: task.validate_output(result) for task in self.tasks}
        if not all(task_validation.values()):
            return   # Some tasks failed

        # Step 4. Pay the actor

        # Step 5. Accepting the work and do the final update as requested
        for task in self.tasks:
            if isinstance(task, Produce):
                # Case Produce Task, save the result as knowledge node
                task_result_value = task.parse_output(result)
                KnowledgeNode(target=self.target, key=task.target, value=task_result_value).save()

        # Step 6. Close the mission as it is accomplished
        self.close()
