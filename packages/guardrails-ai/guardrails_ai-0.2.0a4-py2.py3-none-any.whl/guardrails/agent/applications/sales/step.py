from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from guardrails.agent.step import Action

from .prompts import uninterested_prompt
from .utils import match_step_with_classification_prompt

if TYPE_CHECKING:
    from .state import SalesAgentState

"""
Define the actions available to the agent by subclassing `Action`.

These may also be available to other agents that are part of the same
application e.g. both the user and the agent may be able to send messages.
"""


class UpdateConversationStage(Action):
    agent: str = "agent"
    stage: str = Field(default="1", description="The stage of the conversation.")

    def apply(self, state: "SalesAgentState", **kwargs) -> "SalesAgentState":
        """
        Apply the action to the state, returning a new state.
        """
        state.conversation_stage = self.stage
        state.last_action = self
        return state


class Message(BaseModel):
    text: str = Field(..., description="The message text.")


class SendMessage(Action):
    message: Message = Field(default_factory=Message)

    def message_expresses_disinterest(self, state: "SalesAgentState") -> bool:
        """
        Update the customer disinterest count, by analyzing
        the customer's message.
        """
        last_message = state.trajectory.last_message()
        if last_message:
            dialog = f"({last_message.agent}): {last_message.message.text}\n{self.agent}: {self.message.text}"
        else:
            dialog = self.message.text
        return match_step_with_classification_prompt(
            step=self,
            prompt=uninterested_prompt,
            fill_fn=lambda step: dict(dialog=dialog),
        )

    def apply(self, state: "SalesAgentState", **kwargs) -> "SalesAgentState":
        """
        Apply the action to the state, returning a new state.
        """
        if self.agent == "human":
            disinterested = self.message_expresses_disinterest(state)
            if not disinterested:
                state.customer_disinterest_count = 0
            else:
                state.customer_disinterest_count += 1
        elif self.agent == "agent":
            # Update the last action only if the agent is sending a message.
            state.last_action = self

        state.trajectory.append(self)
        return state


class Skip(Action):
    agent: str = "gasket"

    def apply(self, state: "SalesAgentState", **kwargs) -> "SalesAgentState":
        state.trajectory.append(self)
        return state
