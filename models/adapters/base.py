"""
Model Adapter Base Abstract Class for Local LLMs
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class CompletionRequest(BaseModel):
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 1024
    stop_sequences: List[str] = []

class CompletionResponse(BaseModel):
    content: str
    model: str
    finish_reason: str = "stop"
    usage: Dict[str, int] = {}

class ModelAdapter(ABC):
    @abstractmethod
    async def generate_completion(self, request: CompletionRequest) -> CompletionResponse:
        pass

    @abstractmethod
    async def is_healthy(self) -> bool:
        pass
