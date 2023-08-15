from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel, Extra

from guardrails.agent.state import State
from guardrails.agent.step import Action


class Agent(BaseModel):
    """The base class for all agents."""

    class Config:
        extra = Extra.allow

    @abstractmethod
    def reset(self, **kwargs) -> State:
        """Reset the agent by creating an initial state."""
        raise NotImplementedError

    def ready(self, state: State, **kwargs) -> bool:
        """Check if the agent is ready to propose an action."""
        return True

    @abstractmethod
    def propose(self, state: State, **kwargs) -> Optional[Action]:
        """
        Propose an action for the agent to take.

        Return `None` if the agent should terminate.
        """
        raise NotImplementedError

    def execute(self, state: State, action: Action, **kwargs) -> State:
        """Execute an action in the environment."""
        return action.apply(state)
