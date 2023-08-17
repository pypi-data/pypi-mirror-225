from xia_gpt_prompts.task import Task, Produce
from xia_gpt_prompts.mission import Mission
from xia_gpt_prompts.knowledge import KnowledgeNode
from xia_gpt_prompts.actor import Actor, GptActor
from xia_gpt_prompts.dialog import Dialog, Turn
from xia_gpt_prompts.campaign import Campaign

__all__ = [
    "Task", "Produce",
    "Mission",
    "KnowledgeNode",
    "Actor", "GptActor",
    "Dialog", "Turn",
    "Campaign"
]

__version__ = "0.0.10"