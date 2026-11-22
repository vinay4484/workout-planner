from dataclasses import dataclass, asdict


@dataclass
class LLMMessage:
    role: str
    content: str


@dataclass
class LLMRequest:
    model: str
    messages: list[LLMMessage]
    temperature: float = 0.4

    def to_dict(self) -> dict:
        return asdict(self)