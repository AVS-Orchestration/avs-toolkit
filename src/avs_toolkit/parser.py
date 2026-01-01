import re
import yaml

def parse_markdown_story(content: str) -> dict:
    """
    Standardized AVS Parser v1.6.
    
    Priority Logic:
    1. Look for fenced ```yaml ... ``` blocks. If found, extract and parse ONLY those.
    2. Fallback: Strip headers/guide blocks and parse the raw Markdown text as YAML (Hybrid mode).
    """
    # Normalize line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # --- STRATEGY 1: FENCED YAML BLOCKS ---
    # This looks for blocks tagged specifically with 'yaml'
    yaml_blocks = re.findall(r'```yaml\s*\n(.*?)\n\s*```', content, re.DOTALL)
    
    if yaml_blocks:
        # Combine content from all YAML blocks in the file
        clean_yaml = "\n".join(yaml_blocks)
    else:
        # --- STRATEGY 2: HYBRID FALLBACK ---
        # 1. Remove entire code blocks (including Architect Guides)
        clean_yaml = re.sub(r'```[\s\S]*?```', '', content)
        # 2. Comment out Markdown headers so they don't break YAML keys
        clean_yaml = re.sub(r'^(#+.*)$', r'# \1', clean_yaml, flags=re.MULTILINE)
    
    data = {}

    try:
        yaml_data = yaml.safe_load(clean_yaml)
        if isinstance(yaml_data, dict):
            # Metadata extraction
            meta = yaml_data.get('metadata', {})
            data['metadata'] = {
                "story_id": str(yaml_data.get('story_id') or meta.get('story_id', "VS-UNKNOWN")),
                "version": str(meta.get('version', "1.6")),
                "author": meta.get('author'),
                "status": meta.get('status', 'draft'),
                "provider": meta.get('provider', 'ollama'),
                "preferred_model": meta.get('preferred_model'),
                "assembled_at": meta.get('assembled_at')
            }

            # Goal extraction
            goal_raw = yaml_data.get('goal', {})
            if isinstance(goal_raw, dict):
                data['goal'] = {
                    "as_a": goal_raw.get('as_a', "As a user"),
                    "i_want": goal_raw.get('i_want') or goal_raw.get('outcome_statement', ""),
                    "so_that": goal_raw.get('so_that', "value is created.")
                }
            
            # Instructions extraction
            instr_raw = yaml_data.get('instructions', {})
            steps = []
            reasoning = "Chain-of-Thought"
            
            if isinstance(instr_raw, dict):
                reasoning = instr_raw.get('reasoning_pattern', reasoning)
                raw_steps = instr_raw.get('execution_steps') or instr_raw.get('steps', [])
            elif isinstance(instr_raw, list):
                raw_steps = instr_raw
            else:
                raw_steps = []

            for i, s in enumerate(raw_steps, 1):
                if isinstance(s, dict):
                    steps.append({
                        "step_number": s.get('step', i),
                        "action": str(s.get('action', "")),
                        "validation_rule": str(s.get('validation_rule') or s.get('rule', "Verified."))
                    })
            
            data['instructions'] = {
                "reasoning_pattern": reasoning,
                "execution_steps": steps
            }

            # MCP Servers
            data['mcp_servers'] = yaml_data.get('mcp_servers', [])

            # Context Manifest
            context_raw = yaml_data.get('context_manifest') or yaml_data.get('context', {}).get('mandatory_assets', [])
            assets = []
            if isinstance(context_raw, list):
                for item in context_raw:
                    if isinstance(item, dict):
                        assets.append({
                            "key": item.get('key'),
                            "description": item.get('description'),
                            "default_path": item.get('default_path'),
                            "search_query": item.get('search_query'),
                            "mcp_tool_name": item.get('mcp_tool_name'),
                            "mcp_tool_args": item.get('mcp_tool_args', {})
                        })
                    else:
                        assets.append({"default_path": str(item)})
            data['context_manifest'] = assets

            # Product extraction
            product_raw = yaml_data.get('product', {})
            if isinstance(product_raw, dict):
                data['product'] = {
                    "type": product_raw.get('type', "Document"),
                    "format": product_raw.get('format', "Markdown"),
                    "output_path": product_raw.get('output_path', "outputs"),
                    "handoff_target": product_raw.get('handoff_target')
                }

            # Final verification of minimum requirements
            if data.get('goal', {}).get('i_want') and len(data['instructions']['execution_steps']) > 0:
                return data
    except Exception:
        # Fail gracefully if YAML is totally malformed
        pass

    return data