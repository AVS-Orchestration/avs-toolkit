import os
import httpx
import base64
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

mcp = FastMCP("AVS-GitHub-Context")

@mcp.resource("github://{owner}/{repo}/{path}")
async def get_github_content(owner: str, repo: str, path: str) -> str:
    token = os.getenv("GITHUB_PAT")
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            content_b64 = response.json().get("content", "")
            return base64.b64decode(content_b64).decode("utf-8")
        return f"ERROR: Status {response.status_code}"

@mcp.tool()
async def release_product_to_github(repo_full_name: str, path: str, content: str, commit_message: str):
    token = os.getenv("GITHUB_PAT")
    url = f"https://api.github.com/repos/{repo_full_name}/contents/{path}"
    headers = {"Authorization": f"token {token}"}
    async with httpx.AsyncClient() as client:
        get_res = await client.get(url, headers=headers)
        sha = get_res.json().get("sha") if get_res.status_code == 200 else None
        payload = {
            "message": commit_message,
            "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        }
        if sha: payload["sha"] = sha
        put_res = await client.put(url, json=payload, headers=headers)
        return f"Result: {put_res.status_code}"

if __name__ == "__main__":
    mcp.run()
