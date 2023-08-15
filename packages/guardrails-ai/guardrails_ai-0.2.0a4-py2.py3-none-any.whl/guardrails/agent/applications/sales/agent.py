from guardrails import PromptCallable
from guardrails.agent.agent import Agent
from guardrails.agent.state import State
from guardrails.agent.step import Action
from guardrails.llm_providers import openai_chat_wrapper
from pydantic import Field

from .prompts import goodbye_prompt
from .state import (
    Message,
    SalesAgentState,
    SendMessage,
)
from .step import UpdateConversationStage
from .utils import (
    match_step_with_classification_prompt,
)


class SalesAgent(Agent):
    """
    A sales agent.
    """

    # Custom fields.
    # LLM to use for generating agent actions.
    llm: PromptCallable = Field(default=PromptCallable(openai_chat_wrapper))

    def reset(self) -> SalesAgentState:
        """Reset the agent by creating an initial state."""
        return SalesAgentState()

    def agent_said_goodbye(self, action: SendMessage) -> bool:
        """Return whether the agent said goodbye."""
        return match_step_with_classification_prompt(
            step=action,
            prompt=goodbye_prompt,
            fill_fn=lambda step: dict(dialog=step.message.text),
        )

    def propose(self, state: SalesAgentState) -> Action:
        """Propose an action."""
        # The agent alternates between Message and UpdateConversationStage actions.
        # If the agent said goodbye in its last message, return None.
        if (
            state.last_action
            and isinstance(state.last_action, SendMessage)
            and self.agent_said_goodbye(state.last_action)
        ):
            return None
        if not state.last_action or isinstance(
            state.last_action, UpdateConversationStage
        ):
            return SendMessage(
                agent="agent",
                message=Message(text=self.generate_agent_message(state)),
            )
        elif isinstance(state.last_action, SendMessage):
            return UpdateConversationStage(
                stage=self.determine_conversation_stage(state),
            )
        else:
            raise ValueError("Invalid last action.")

    def determine_conversation_stage(self, state: SalesAgentState) -> str:
        """
        Generate the next conversation stage.
        """
        stage = self.llm(
            str(
                state.config.analysis_prompt.format(
                    conversation_history=state.trajectory.history(),
                    current_conversation_stage=state.conversation_stage,
                )
            ),
            max_tokens=1,
            temperature=0.9,
        )
        # Ensure that the stage is valid, otherwise return the current stage.
        if stage not in state.config.conversation_stages:
            return state.conversation_stage
        return stage

    def generate_agent_message(self, state: SalesAgentState) -> str:
        """
        Generate an agent message.
        """
        config = state.config
        prompt = config.prompt.format(
            salesperson_name=config.salesperson_name,
            salesperson_role=config.salesperson_role,
            company_name=config.company_name,
            company_business=config.company_business,
            company_values=config.company_values,
            conversation_purpose=config.conversation_purpose,
            conversation_type=config.conversation_type,
            conversation_stage=config.conversation_stages[state.conversation_stage],
            conversation_history=state.trajectory.history(),
        )
        return self.llm(str(prompt), temperature=0.9, stop=["<END_OF_TURN>"])

    def execute(self, state: State, action: Action) -> State:
        """Execute an action."""
        if isinstance(action, SendMessage):
            print(f"Agent is messaging: {action.message.text}")
        elif isinstance(action, UpdateConversationStage):
            print(f"Updating conversation stage to: {action.stage}")
        return action.apply(state)
