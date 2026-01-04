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
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token and token.strip() and not token.startswith("your_"):
        headers["Authorization"] = f"token {token.strip()}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            content_b64 = response.json().get("content", "")
            return base64.b64decode(content_b64).decode("utf-8")
        elif response.status_code == 401:
            return f"ERROR: Unauthorized (401). Please check your GITHUB_PAT in .env."
        elif response.status_code == 404:
            return f"ERROR: Not Found (404). Check if the repo/path '{owner}/{repo}/{path}' is correct."
        return f"ERROR: Status {response.status_code} - {response.text}"

@mcp.tool()
async def create_github_issue(owner: str, repo: str, title: str, body: str, labels: list[str] = []) -> str:
    """
    Creates a new issue in a GitHub repository.
    Args:
        owner: The GitHub user or organization name.
        repo: The repository name.
        title: The title of the issue.
        body: The detailed description of the issue (Markdown supported).
        labels: A list of labels to apply to the issue (e.g., ['bug', 'enhancement']).
    """
    token = os.getenv("GITHUB_PAT")
    if not token or token.startswith("your_"):
        return "ERROR: GITHUB_PAT not configured. Issue creation requires an API token."

    url = f"https://api.github.com/repos/{owner}/{repo}/issues"
    headers = {
        "Authorization": f"token {token.strip()}",
        "Accept": "application/vnd.github.v3+json"
    }
    payload = {"title": title, "body": body, "labels": labels}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            issue_url = response.json().get("html_url")
            return f"SUCCESS: Issue created at {issue_url}"
        return f"ERROR: Status {response.status_code} - {response.text}"

@mcp.tool()
async def fetch_github_file(owner: str, repo: str, path: str) -> str:
    """
    Fetches the raw text content of a file from a GitHub repository.
    Args:
        owner: The GitHub user or organization name.
        repo: The repository name.
        path: The path to the file within the repository (e.g., 'README.md' or 'src/main.py').
    """
    return await get_github_content(owner, repo, path)

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
