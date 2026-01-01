import httpx
from rich.console import Console
from .base import LLMProvider

console = Console()

class OllamaProvider(LLMProvider):
    """
    Provider for local Ollama execution.
    """
    async def generate(self, system_prompt: str, user_payload: str, model: str) -> str:
        base_url = "http://127.0.0.1:11434"
        generate_url = f"{base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": user_payload,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2
            }
        }

        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(generate_url, json=payload)
                
                if response.status_code == 404:
                    console.print(f"[red]Error:[/red] Ollama endpoint not found.")
                    return None
                elif response.status_code == 400:
                    console.print(f"[red]Error:[/red] Bad request. Does model '{model}' exist? Run 'ollama pull {model}'")
                    return None
                    
                response.raise_for_status()
                result = response.json()
                return result.get("response", "")
                
        except httpx.ConnectError:
            console.print(f"[red]Error:[/red] Could not connect to Ollama. Is the app running?")
            return None
        except Exception as e:
            console.print(f"[red]Error communicating with Ollama:[/red] {e}")
            return None
