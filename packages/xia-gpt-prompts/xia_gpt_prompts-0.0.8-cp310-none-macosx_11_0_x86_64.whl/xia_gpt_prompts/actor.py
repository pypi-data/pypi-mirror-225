from xia_gpt import Gpt
from xia_gpt_openai import OpenaiGpt
from xia_gpt_prompts.mission import Mission


class Actor:
    def __init__(self):
        self.agent = OpenaiGpt()  # Default Actor is GPT 3.5

    def evaluate_mission(self,
                         profile: str,
                         mission: Mission,
                         budget: float = None) -> bool:
        """Evaluate work to see we could take the mission or not

        Args:
            profile: The profile needed
            mission: Mission object
            budget: whether the budget could cover the cost

        Returns:
            True if accept mission
        """
        if not budget:
            return True
        return False  # By default deny

    async def execute_mission(self, profile: str, mission: Mission) -> dict:
        """Execute the mission

        Args:
            profile: The profile needed
            mission: Mission object

        Returns:
            A dictionary about the run result
        """
        prompt = mission.get_prompt(profile)
        result, job_status = await self.agent.chat_complete_stream("", prompt)
        return {"status": "successful", "result": result, "cost": job_status}


