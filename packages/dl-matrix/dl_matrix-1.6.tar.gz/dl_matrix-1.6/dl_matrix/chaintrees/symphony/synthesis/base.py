from abc import ABC, abstractmethod
from typing import Any, Dict


class SynthesisTechnique(ABC):
    def __init__(
        self,
        epithet: str,
        name: str,
        technique_name: str,
        imperative: str,
        prompts: Dict[str, Any],
    ):
        self.epithet = epithet
        self.name = name
        self.technique_name = technique_name
        self.imperative = imperative
        self.prompts = prompts

    @abstractmethod
    def execute(self, *args, **kwargs) -> None:
        pass

    def get_options(self) -> Dict[str, Any]:
        return {
            "epithet": self.epithet,
            "name": self.name,
            "technique_name": self.technique_name,
            "imperative": self.imperative,
            "prompts": self.prompts,
        }
