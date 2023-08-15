from typing import TYPE_CHECKING, List

from pydantic import BaseModel, Field
from rich import print

from guardrails.agent.scenario import Scenario

if TYPE_CHECKING:
    from guardrails.agent.state import State
    from guardrails.agent.step import Action


class AgentGuard(BaseModel):
    scenarios: List[Scenario] = Field(default_factory=list)

    def run_validation(
        self,
        state: "State",
        action: "Action",
        **kwargs,
    ) -> "Action":
        """Validate an action using the scenarios."""

        if action is None:
            return action

        for scenario in self.scenarios:
            print(f"\t> Running scenario {scenario.name}")
            if scenario.recognize(state, action):
                print("\t>> Recognized")
                new_action = scenario.run_validation(state, action)
                if action != new_action:
                    print("\t>> Failed validation")
                    return new_action
                print("\t>> Passed validation")
            else:
                print("\t>> Skipping")

        return action
