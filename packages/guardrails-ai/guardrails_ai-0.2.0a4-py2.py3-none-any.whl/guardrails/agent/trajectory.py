from typing import Callable, List

from pydantic import BaseModel, Field

from guardrails.agent.step import Step


class Trajectory(BaseModel):
    # Descriptive name for the trajectory
    name: str

    # The list of steps in the trajectory
    data: List[Step] = Field(default_factory=list)

    def append(self, step: Step) -> None:
        """Add a step to the trajectory."""
        assert isinstance(step, Step), "Can only append a `Step` to a trajectory."
        self.data.append(step)

    def extend(self, steps: List[Step]) -> None:
        """Add a list of steps to the trajectory."""
        assert all(
            isinstance(step, Step) for step in steps
        ), "Can only extend a `Trajectory` with a list of `Step`s."
        self.data.extend(steps)

    def list(self, format: str = None):
        return [x.dict(format) for x in self.data]

    def __len__(self):
        return len(self.data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__class__(name=self.name, data=self.data[key])
        elif isinstance(key, list):
            return self.__class__(name=self.name, data=[self.data[i] for i in key])
        else:
            return self.data[key]

    def itemize(
        self,
        format_fn: Callable[[Step], str] = None,
        skip_fn: Callable[[Step], bool] = None,
        use_prefix: bool = True,
    ) -> str:
        """
        Returns a string representation of the trajectory as a list of items.

        Args:
            format_fn: Function that formats a step into a string.
            skip_fn: Function that returns True if a step should be skipped.
            use_prefix: Whether to use a prefix for each item.
        """
        if skip_fn is None:

            def skip_fn(step: Step) -> bool:
                return False

        if format_fn is None:

            def format_fn(step: Step) -> str:
                return f"({step.agent}): {step.params['summary']}"

        items = []
        for step in self.data:
            if skip_fn(step):
                continue
            try:
                format_str = format_fn(step)
            except KeyError as e:
                raise KeyError(
                    f"Format function is missing key {e} for step {step}. "
                    "Try using a different format function, or use a skip function."
                )
            if use_prefix:
                items.append(f"T{len(items)+1}. {format_str}")
            else:
                items.append(format_str)
        return "\n".join(items)
