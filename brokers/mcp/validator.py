"""
MCP Tool Schema and Permission Validator
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel

class McpToolDefinition(BaseModel):
    name: str
    description: str
    is_mutating: bool = False
    required_state: str = "NORMAL" # Minimum required state (NORMAL, WATCH, RESTRICTED)

REGISTERED_MCP_TOOLS: Dict[str, McpToolDefinition] = {
    "local_code_search": McpToolDefinition(name="local_code_search", description="Search indexed code in workspace", is_mutating=False),
    "ast_analyzer": McpToolDefinition(name="ast_analyzer", description="Parse Python AST nodes", is_mutating=False),
    "local_git_status": McpToolDefinition(name="local_git_status", description="Query git repo status", is_mutating=False),
    "local_git_commit": McpToolDefinition(name="local_git_commit", description="Create local git commit", is_mutating=True),
}
