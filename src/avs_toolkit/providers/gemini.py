import os
import httpx
from rich.console import Console
from .base import LLMProvider

console = Console()

class GeminiProvider(LLMProvider):
    """
    Provider for Google Gemini API.
    Requires GEMINI_API_KEY environment variable.
    """
    async def generate(self, system_prompt: str, user_payload: str, model: str) -> str:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            console.print("[red]Error:[/red] GEMINI_API_KEY not found in environment variables.")
            return None

        # Gemini API expects the model name in the URL
        # e.g., "gemini-1.5-flash" or "gemini-1.5-pro"
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        # Construct Gemini payload
        # System instructions are supported in v1beta for some models, but simpler to append to prompt for broad compatibility
        # unless specifically using the systemInstruction field.
        # Let's use the systemInstruction field for better adherence.
        
        payload = {
            "systemInstruction": {
                "parts": [
                    {"text": system_prompt}
                ]
            },
            "contents": [
                {
                    "parts": [
                        {"text": user_payload}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }

        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                response = await client.post(url, json=payload)
                
                if response.status_code != 200:
                    console.print(f"[red]Error (Gemini):[/red] {response.status_code} - {response.text}")
                    return None
                    
                result = response.json()
                # Extract text from response
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0].get('content', {})
                    parts = content.get('parts', [])
                    if parts:
                        return parts[0].get('text', "")
                
                return ""
                
        except Exception as e:
            console.print(f"[red]Error communicating with Gemini:[/red] {e}")
            return None
