import pytest
from unittest.mock import MagicMock
from avs_toolkit.providers.ollama import OllamaProvider
from avs_toolkit.providers.gemini import GeminiProvider

@pytest.mark.asyncio
async def test_ollama_provider_call(mocker):
    """Test that OllamaProvider posts to the correct localhost URL."""
    mock_post = mocker.patch("httpx.AsyncClient.post", return_value=MagicMock(status_code=200, json=lambda: {"response": "Ollama says hi"}))
    
    provider = OllamaProvider()
    response = await provider.generate("System", "User Payload", "llama3")
    
    assert response == "Ollama says hi"
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == "http://127.0.0.1:11434/api/generate"
    assert kwargs['json']['model'] == "llama3"

@pytest.mark.asyncio
async def test_gemini_provider_call(mocker, monkeypatch):
    """Test that GeminiProvider posts to the Google API URL and uses the API key."""
    monkeypatch.setenv("GEMINI_API_KEY", "test-key-123")
    
    mock_response = MagicMock(status_code=200)
    mock_response.json.return_value = {
        "candidates": [
            {"content": {"parts": [{"text": "Gemini says hello"}]}}
        ]
    }
    mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)
    
    provider = GeminiProvider()
    response = await provider.generate("System", "User Payload", "gemini-1.5-flash")
    
    assert response == "Gemini says hello"
    # Verify URL structure contains model and key
    args, kwargs = mock_post.call_args
    assert "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent" in args[0]
    assert "key=test-key-123" in args[0]
