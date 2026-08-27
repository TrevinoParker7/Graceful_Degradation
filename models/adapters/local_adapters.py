"""
Local Model Adapters for Ollama, LM Studio, llama.cpp, and Local OpenAI-Compatible APIs
"""

import httpx
from typing import Optional
from .base import CompletionRequest, CompletionResponse, ModelAdapter

class OllamaAdapter(ModelAdapter):
    def __init__(self, base_url: str = "http://127.0.0.1:11434", model: str = "qwen2.5-coder"):
        self.base_url = base_url
        self.model = model

    async def generate_completion(self, request: CompletionRequest) -> CompletionResponse:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": self.model, "prompt": request.prompt, "stream": False},
                )
                if res.status_code == 200:
                    data = res.json()
                    return CompletionResponse(content=data.get("response", ""), model=self.model)
        except Exception:
            pass
        return CompletionResponse(content="[Local Ollama Offline Fallback]", model=self.model)

    async def is_healthy(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/api/tags")
                return res.status_code == 200
        except Exception:
            return False

class LMStudioAdapter(ModelAdapter):
    def __init__(self, base_url: str = "http://127.0.0.1:1234/v1", model: str = "local-model"):
        self.base_url = base_url
        self.model = model

    async def generate_completion(self, request: CompletionRequest) -> CompletionResponse:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": request.prompt}],
                        "temperature": request.temperature,
                    },
                )
                if res.status_code == 200:
                    data = res.json()
                    return CompletionResponse(
                        content=data["choices"][0]["message"]["content"], model=self.model
                    )
        except Exception:
            pass
        return CompletionResponse(content="[LM Studio Offline Fallback]", model=self.model)

    async def is_healthy(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/models")
                return res.status_code == 200
        except Exception:
            return False

class LlamaCppAdapter(ModelAdapter):
    def __init__(self, base_url: str = "http://127.0.0.1:8080", model: str = "llama-cpp"):
        self.base_url = base_url
        self.model = model

    async def generate_completion(self, request: CompletionRequest) -> CompletionResponse:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/completion",
                    json={"prompt": request.prompt, "n_predict": request.max_tokens},
                )
                if res.status_code == 200:
                    data = res.json()
                    return CompletionResponse(content=data.get("content", ""), model=self.model)
        except Exception:
            pass
        return CompletionResponse(content="[llama.cpp Offline Fallback]", model=self.model)

    async def is_healthy(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/health")
                return res.status_code == 200
        except Exception:
            return False

class OpenAICompatibleLocalAdapter(ModelAdapter):
    def __init__(self, base_url: str = "http://127.0.0.1:8000/v1", model: str = "default"):
        self.base_url = base_url
        self.model = model

    async def generate_completion(self, request: CompletionRequest) -> CompletionResponse:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                res = await client.post(
                    f"{self.base_url}/chat/completions",
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": request.prompt}],
                    },
                )
                if res.status_code == 200:
                    data = res.json()
                    return CompletionResponse(
                        content=data["choices"][0]["message"]["content"], model=self.model
                    )
        except Exception:
            pass
        return CompletionResponse(content="[OpenAI Local API Offline Fallback]", model=self.model)

    async def is_healthy(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                res = await client.get(f"{self.base_url}/models")
                return res.status_code == 200
        except Exception:
            return False
