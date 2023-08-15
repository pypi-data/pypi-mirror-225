from guardrails.agent.state import State
from guardrails.agent.step import Action
from pydantic import BaseModel


class AgentValidator(BaseModel):
    """Base class for agent validators."""

    @property
    def name(self):
        """Name of the validator."""
        return self.__class__.__name__

    def __call__(self, state: State, action: Action) -> bool:
        """Validate an action given the current state."""
        raise NotImplementedError
