import uuid
from xia_gpt import Gpt
from xia_gpt_openai import OpenaiGpt
from xia_gpt_prompts.mission import Mission


class Actor:
    def __init__(self, name: str = None, **kwargs):
        self.name = str(uuid.uuid4()) if not name else name

    def evaluate_mission(self,
                         profile: str,
                         request: str,
                         budget: float = None) -> bool:
        """Evaluate work to see we could take the mission or not

        Args:
            profile: The profile needed
            request: request to be done
            budget: whether the budget could cover the cost

        Returns:
            True if accept mission
        """
        return True


class GptActor(Actor):
    def __init__(self, name: str = None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.agent = OpenaiGpt()  # Default GPT Actor is GPT 3.5

    def evaluate_mission(self,
                         profile: str,
                         request: str,
                         budget: float = None) -> bool:
        if not budget:
            return True
        return False  # By default deny

    async def execute_mission(self, profile: str, request: str) -> dict:
        """Execute the mission

        Args:
            profile: The profile needed
            request: request to be done

        Returns:
            A dictionary about the run result
        """
        result, job_status = await self.agent.chat_complete_stream("", request)
        return {"status": "successful", "result": result, "cost": job_status}


