from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, validator

if TYPE_CHECKING:
    from guardrails.agent import State


class Step(BaseModel):
    """A step in a trajectory."""

    # Agent relevant to the step
    agent: str = Field(..., alias="agent")

    # What kind of step is this?
    kind: str = Field(..., alias="type")

    def to_dict(self, format: str = None):
        if format == "chatgpt" or format == "dialog":
            return {
                "role": self.agent,
                "content": self.content,
            }
        elif format == "summary":
            return {
                "agent": self.agent,
                "content": self.summary if "summary" in self else self.content,
            }
        return {
            "agent": self.agent,
            **self.dict(exclude={"agent"}),
        }

    def has_type(self, t: type) -> bool:
        """Check if the step has the given type."""
        return isinstance(self, t)

    def apply(self, state: "State", **kwargs) -> "State":
        """Apply the step to a given state."""
        raise NotImplementedError


class Action(Step):
    """Class for representing an action in a trajectory."""

    kind: str = "action"

    @validator("kind")
    def kind_must_be_action(cls, v):
        assert v == "action", "Kind must be 'action'."
        return v

    def apply(self, state: "State", **kwargs) -> "State":
        """Apply the action to a given state."""
        raise NotImplementedError


class Observation(Step):
    """Class for representing an observation in a trajectory."""

    kind: str = "observation"

    @validator("kind")
    def kind_must_be_observation(cls, v):
        assert v == "observation", "Kind must be 'observation'."
        return v


class ValidatorStep(Step):
    """Class for representing a validator step in a trajectory."""

    agent: str = "gasket"
    kind: str = "validation"
    name: str
    action: Action
    new_action: Action

    def apply(self, state: "State", **kwargs) -> "State":
        assert hasattr(
            state, "trajectory"
        ), "State must have a trajectory attribute to apply a ValidatorStep."
        state.trajectory.append(self)
        return state
