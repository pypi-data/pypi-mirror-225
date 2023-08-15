from pydantic import BaseModel, Field

from guardrails.agent.step import Action, Step


class State(BaseModel):
    """The state of a single agent."""

    class Config:
        arbitrary_types_allowed = True

    # Config associated with this agent.
    config: dict = Field(default_factory=dict)

    def tick(self, step: Step, **kwargs) -> "State":
        """A tick is a single step in the environment.

        Ticks on this agent's state should happen when:
            - the environment updates due to some external factor
            - another agent observes some information or takes an action

        The tick method should update and return the new state of this agent.
        """
        return step.apply(self)

    def apply(self, action: Action, **kwargs) -> "State":
        """
        Apply an action to update this agent's state.

        Implement this method to update the state of the agent
        when it takes an action.
        """
        return action.apply(self)
