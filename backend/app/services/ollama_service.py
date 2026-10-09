from __future__ import annotations

import httpx

from app.config import DEFAULT_MODEL, OLLAMA_BASE_URL


class OllamaService:
    def __init__(self, base_url: str = OLLAMA_BASE_URL) -> None:
        self.base_url = base_url.rstrip('/')

    async def check_connection(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(f'{self.base_url}/api/tags')
                return response.is_success
        except Exception:
            return False

    async def list_models(self) -> list[str]:
        try:
            async with httpx.AsyncClient(timeout=20) as client:
                response = await client.get(f'{self.base_url}/api/tags')
                if response.status_code >= 400:
                    return []
                payload = response.json()
                models = payload.get('models', [])
                return [item.get('name', '') for item in models if item.get('name')]
        except Exception:
            return []

    async def is_model_available(self, model_name: str) -> bool:
        models = await self.list_models()
        return model_name in models or model_name == DEFAULT_MODEL

    async def generate(self, model_name: str, prompt: str, system_prompt: str | None = None) -> str:
        async with httpx.AsyncClient(timeout=180) as client:
            payload = {
                'model': model_name,
                'prompt': prompt,
                'stream': False,
                'options': {'temperature': 0.2},
            }
            if system_prompt:
                payload['system'] = system_prompt
            response = await client.post(f'{self.base_url}/api/generate', json=payload)
            if response.status_code >= 400:
                raise ValueError(f'Ollama generation failed: {response.text[:250]}')
            data = response.json()
            if isinstance(data.get('response'), str):
                return data['response']
            return str(data)

    async def embed(self, model_name: str, text: str) -> list[float]:
        async with httpx.AsyncClient(timeout=180) as client:
            response = await client.post(
                f'{self.base_url}/api/embed',
                json={'model': model_name, 'input': text},
            )
            if response.status_code >= 400:
                raise ValueError(f'Ollama embed failed: {response.text[:250]}')
            data = response.json()
            if 'embedding' in data:
                return data['embedding']
            if 'embeddings' in data and data['embeddings']:
                return data['embeddings'][0]
            raise ValueError('Embedding data not found in Ollama response')


ollama_service = OllamaService()
