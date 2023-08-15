import inspect
import sys
from typing import Callable, List, Optional, Union

from pydantic import BaseModel, Extra, Field
from rich import print

from guardrails.agent.state import State
from guardrails.agent.step import Action, ValidatorStep
from guardrails.agent.validator import AgentValidator


def get_class_that_defined_method(meth):
    # https://stackoverflow.com/a/25959545
    print(inspect.isfunction(meth))
    print(inspect.getmodule(meth))
    print(meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0])
    print(inspect.getmembers(sys.modules[__name__], inspect.isclass))
    print(inspect.getmembers(inspect.getmodule(meth), inspect.isclass))
    if inspect.isfunction(meth):
        return getattr(
            inspect.getmodule(meth),
            meth.__qualname__.split(".<locals>", 1)[0].rsplit(".", 1)[0],
            None,
        )
    return None


def agentvalidator(func: Callable):
    """Decorator for agent validators."""
    print(func)
    cls = get_class_that_defined_method(func)

    # TODO(karan): this is INCREDIBLY hacky.
    if cls not in agentvalidator.validators:
        agentvalidator.validators[cls.__name__] = []
    agentvalidator.validators[cls.__name__].append(func)

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


agentvalidator.validators = {}


class Scenario(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        extra = Extra.allow

    # Scenario name, single word
    name: str

    # Description of the scenario
    description: Optional[str] = None

    # List of validators for this scenario
    validators: List[Union[Callable, AgentValidator]] = Field(default_factory=list)

    # Recognition function
    recfn: Callable = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.recfn:
            self.recognize = self.recfn

        # self.validators.extend(
        #     [
        #         partial(v, self)
        #         for v in agentvalidator.validators[self.__class__.__name__]
        #     ]
        # )

    def recognize(self, state: State, action: Action) -> bool:
        """Recognize whether the trajectory matches this scenario."""
        raise NotImplementedError

    def run_validation(self, state: State, action: Action) -> Action:
        """Validate the trajectory using the validators."""
        # TODO: return more information.
        for validator in self.validators:
            new_action = validator(state, action)
            if new_action != action:
                step = ValidatorStep(
                    name=validator.name,
                    action=action,
                    new_action=new_action,
                )
                print(f"\t\t>> Validator failed:\n\t\t{step}\n")
                state = step.apply(state)
                return new_action
        return action

    @classmethod
    def from_description(cls, name: str) -> "Scenario":
        return cls(name=name)

    @classmethod
    def from_examples(cls, name: str, examples: List[str]) -> "Scenario":
        return cls(name=name, examples=examples)

    @classmethod
    def on_propose(
        cls, action_cls: type, validators: List[Union[Callable, AgentValidator]]
    ) -> "Scenario":
        return cls(
            name=f"on_propose_{action_cls.__name__}",
            description=f"When the agent proposes the {action_cls.__name__} action",
            validators=validators,
            recfn=lambda state, action: isinstance(action, action_cls),
        )
