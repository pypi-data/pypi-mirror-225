from pydantic import Field

from guardrails.agent import Action, AgentValidator, Scenario, State, Step
from guardrails.agent.applications.sales.prompts import (
    disinterested_thanks_and_bye_prompt,
    polite_prompt,
    question_prompt,
)
from guardrails.agent.applications.sales.step import SendMessage
from guardrails.agent.applications.sales.utils import (
    match_step_with_classification_prompt,
)

from .step import Skip


class CompetitorCheck(AgentValidator):
    # Names of sleep product competitors.
    COMPETITORS = ["purple", "casper", "tuft and needle", "leesa"]

    def __call__(self, state: State, action: Action) -> Action:
        assert isinstance(action, SendMessage)
        if any(
            competitor in action.message.text.lower() for competitor in self.COMPETITORS
        ):
            return Skip()
        return action


class AgentIsPolite(AgentValidator):
    def __call__(self, state: State, action: Action) -> Action:
        assert isinstance(action, SendMessage)
        if not match_step_with_classification_prompt(
            step=action,
            prompt=polite_prompt,
            fill_fn=lambda step: dict(dialog=step.message.text),
        ):
            return Skip()
        return action


class AgentContinuesConversation(AgentValidator):
    def __call__(self, state: State, action: Action) -> Action:
        assert isinstance(action, SendMessage)
        # if match_step_with_classification_prompt(
        #     step=action,
        #     prompt=disinterested_thanks_and_bye_prompt,
        #     fill_fn=lambda step: dict(dialog=step.message.text),
        # ):
        if not match_step_with_classification_prompt(
            step=action,
            prompt=question_prompt,
            fill_fn=lambda step: dict(dialog=step.message.text),
        ):
            return Skip()
        return action


class AgentRespectfullyEndsConversation(AgentValidator):
    def __call__(self, state: State, action: Action) -> Action:
        assert isinstance(action, SendMessage)
        if not match_step_with_classification_prompt(
            step=action,
            prompt=disinterested_thanks_and_bye_prompt,
            fill_fn=lambda step: dict(dialog=step.message.text),
        ):
            return Skip()
        return action


class ForceAgentToEndConversation(AgentValidator):
    def __call__(self, state: State, action: Action) -> Action:
        if isinstance(action, SendMessage) and action.agent == "agent":
            return SendMessage(
                agent="agent",
                message=dict(
                    text="Thanks for taking the time to chat. Have a great day!"
                ),
            )
        return action


class AgentSendingMessage(Scenario):
    name: str = "agent_sending_message"
    description: str = "The agent is sending a message."
    validators: list = Field(default=[CompetitorCheck()])

    def recognize(self, state: State, action: Action) -> bool:
        return isinstance(action, SendMessage) and action.agent == "agent"


class CustomerDisinterestedOnce(Scenario):
    name: str = "customer_disinterested_once"
    description: str = "The customer has indicated they are not interested once."
    validators: list = Field(default=[AgentIsPolite(), AgentContinuesConversation()])

    def recognize(self, state: State, action: Action) -> bool:
        if state.customer_disinterest_count == 1 and isinstance(action, SendMessage):
            # The customer has indicated they are not interested once,
            # and the agent is sending a message.
            return True
        return False


class CustomerDisinterestedTwice(Scenario):
    name: str = "customer_disinterested_twice"
    description: str = "The customer has indicated they are not interested twice."
    validators: list = Field(default=[AgentRespectfullyEndsConversation()])

    def recognize(self, state: State, action: Action) -> bool:
        if state.customer_disinterest_count == 2 and isinstance(action, SendMessage):
            # The customer has indicated they are not interested twice,
            # and the agent is sending a message.
            return True
        return False


class SkippedTooManyTimes(Scenario):
    name: str = "skipped_too_many_times"
    description: str = "The agent has skipped too many times."
    validators: list = Field(default=[ForceAgentToEndConversation()])

    def recognize(self, state: State, action: Action) -> bool:
        # Check if the agent has been skipping too many times.
        num_skips = 0
        for step in reversed(state.trajectory.data):
            if isinstance(step, Skip):
                num_skips += 1
            elif isinstance(step, Step):
                pass
            else:
                break
        
        if num_skips >= 3:
            return True
        return False
