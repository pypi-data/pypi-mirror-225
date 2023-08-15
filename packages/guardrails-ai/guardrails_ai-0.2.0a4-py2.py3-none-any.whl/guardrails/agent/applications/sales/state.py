from typing import Optional

from pydantic import BaseModel, Field

from guardrails import Prompt
from guardrails.agent.applications.sales.prompts import (
    sales_agent_inception_prompt,
    stage_analyzer_inception_prompt,
)
from guardrails.agent.applications.sales.step import (
    Message,
    SendMessage,
)
from guardrails.agent import Action, State, Trajectory

"""
Define a trajectory for the application by subclassing `Trajectory`.

This defines the sequence of steps that happen in the application.
Steps can be actions, or any other type of custom step that you want to track
e.g. observations made by particular agents.
"""


class SalesConversation(Trajectory):
    """A sales conversation."""

    name: str = "sales_conversation"

    def warm_start(
        self,
        salesperson_name: str,
        company_name: str,
    ) -> "SalesConversation":
        """Define a custom method to warm start the conversation."""
        assert len(self) == 0, "Can only warm start an empty conversation."
        actions = [
            SendMessage(
                agent="agent",
                message=Message(
                    text=f"Hi, this is {salesperson_name} from {company_name}. "
                    "How are you doing today? <END_OF_TURN>"
                ),
            ),
            SendMessage(
                agent="human",
                message=Message(text="I'm well, how are you? <END_OF_TURN>"),
            ),
        ]
        self.extend(actions)

        return self

    def history(self) -> str:
        """A custom method to produce a string representation of the conversation."""
        return self.itemize(
            format_fn=lambda step: f"({step.agent}): {step.message.text}",
            skip_fn=lambda step: not isinstance(step, SendMessage),
            use_prefix=False,
        )
    
    def last_message(self) -> Optional[SendMessage]:
        """Get the last message in the conversation."""
        for step in reversed(self.data):
            if isinstance(step, SendMessage):
                return step
        return None


"""
Define the state of the agent by subclassing `State`. The state contains
all the information that the agent needs to make decisions e.g. the
configuration of the agent, the current stage of the conversation, etc.

Below, we define a SalesAgentConfig class that defines the configuration
for the agent (which is one field of the state).
"""


class SalesAgentConfig(BaseModel):
    """A configuration for the sales agent."""

    class Config:
        arbitrary_types_allowed = True

    salesperson_name: str = "Ted Lasso"
    salesperson_role: str = "Business Development Representative"
    company_name: str = "Sleep Haven"
    company_business: str = "Sleep Haven is a premium mattress company that provides customers with the most comfortable and supportive sleeping experience possible. We offer a range of high-quality mattresses, pillows, and bedding accessories that are designed to meet the unique needs of our customers."  # noqa: E501
    company_values: str = "Our mission at Sleep Haven is to help people achieve a better night's sleep by providing them with the best possible sleep solutions. We believe that quality sleep is essential to overall health and well-being, and we are committed to helping our customers achieve optimal sleep by offering exceptional products and customer service."  # noqa: E501
    conversation_purpose: str = "find out whether they are looking to achieve better sleep via buying a premier mattress."  # noqa: E501
    conversation_type: str = "call"

    conversation_stages: dict = {
        "1": "Introduction: Start the conversation by introducing yourself and your company. Be polite and respectful while keeping the tone of the conversation professional. Your greeting should be welcoming. Always clarify in your greeting the reason why you are contacting the prospect.",  # noqa: E501
        "2": "Qualification: Qualify the prospect by confirming if they are the right person to talk to regarding your product/service. Ensure that they have the authority to make purchasing decisions.",  # noqa: E501
        "3": "Value proposition: Briefly explain how your product/service can benefit the prospect. Focus on the unique selling points and value proposition of your product/service that sets it apart from competitors.",  # noqa: E501
        "4": "Needs analysis: Ask open-ended questions to uncover the prospect's needs and pain points. Listen carefully to their responses and take notes.",  # noqa: E501
        "5": "Solution presentation: Based on the prospect's needs, present your product/service as the solution that can address their pain points.",  # noqa: E501
        "6": "Objection handling: Address any objections that the prospect may have regarding your product/service. Be prepared to provide evidence or testimonials to support your claims.",  # noqa: E501
        "7": "Close: Ask for the sale by proposing a next step. This could be a demo, a trial or a meeting with decision-makers. Ensure to summarize what has been discussed and reiterate the benefits.",  # noqa: E501
    }

    prompt: Prompt = Field(default=sales_agent_inception_prompt)
    analysis_prompt: Prompt = Field(default=stage_analyzer_inception_prompt)


class SalesAgentState(State):
    """The state of the sales agent."""

    # The configuration of the agent.
    config: SalesAgentConfig = Field(default_factory=SalesAgentConfig)

    # The conversation.
    trajectory: SalesConversation = Field(default_factory=SalesConversation)

    # The stage of the conversation.
    conversation_stage: str = "1"

    # The number of times the customer has expressed disinterest.
    customer_disinterest_count: int = 0

    # The last action taken.
    last_action: Optional[Action] = None

    def step_on_message(self, message: str) -> "SalesAgentState":
        """
        A custom tick to move the state forward on a message.
        """
        return SendMessage(
            agent="human",
            message=Message(text=message + " <END_OF_TURN>"),
        ).apply(self)
