from rich import print

from guardrails.agent import AgentGuard
from guardrails.agent.applications.sales.agent import SalesAgent
from guardrails.agent.applications.sales.state import SendMessage
from guardrails.agent.applications.sales.validators import (
    AgentSendingMessage,
    CustomerDisinterestedOnce,
    CustomerDisinterestedTwice,
    SkippedTooManyTimes,
)
import os
os.environ['OPENAI_API_KEY'] = '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'

agent = SalesAgent()
state = agent.reset()
guard = AgentGuard(
    scenarios=[
        SkippedTooManyTimes(),
        AgentSendingMessage(),
        CustomerDisinterestedOnce(),
        CustomerDisinterestedTwice(),
    ]
)
# Alternately, directly create the scenarios and pass them to the guard.
# Scenario(
#     name="agent_sending_message",
#     description="The agent is sending a message.",
#     validators=[CompetitorCheck(), ...],
#     recfn=lambda state, action: isinstance(action, SendMessage)
#     and action.agent == "agent",
# )


while True:
    print(state.trajectory.history())
    # Propose an agent action.
    action = agent.propose(state)

    # Validate the action.
    action = guard.run_validation(state, action)

    if not action:
        # Terminate if no action is proposed.
        break

    # Finalize and execute the action.
    state = agent.execute(state, action)

    # Tick when an agent message is sent.
    if isinstance(action, SendMessage):
        state = state.step_on_message(input("Enter a message: "))

    # Wait for the agent to be ready.
    while not agent.ready(state):
        pass
