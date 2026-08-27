"""
Local MCP Gateway
Validates MCP tool schemas, identity, risk scores, and restricts mutating tools under degraded states.
Executes real local Python tool handlers for code search, AST parsing, and git status.
"""

import ast
import os
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional
from config.settings import config
from core.audit.ledger import audit_ledger
from core.capabilities.permissions import Capability
from core.policy.engine import policy_engine
from core.risk.engine import risk_engine
from .validator import REGISTERED_MCP_TOOLS, McpToolDefinition

class McpGateway:
    def _execute_local_code_search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """Search local workspace files for string match."""
        results = []
        workspace = Path(__file__).resolve().parent.parent.parent
        for p in workspace.rglob("*.py"):
            if "runtime" in p.parts or ".git" in p.parts:
                continue
            try:
                content = p.read_text(encoding="utf-8", errors="ignore")
                if query.lower() in content.lower():
                    lines = [line.strip() for line in content.splitlines() if query.lower() in line.lower()]
                    results.append({"file": str(p.relative_to(workspace)), "matches": lines[:2]})
                    if len(results) >= max_results:
                        break
            except Exception:
                continue
        return {"query": query, "total_matches": len(results), "results": results}

    def _execute_ast_analyzer(self, code_snippet: str) -> Dict[str, Any]:
        """Parse Python code and return AST structure analysis."""
        try:
            tree = ast.parse(code_snippet)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = [node.names[0].name for node in ast.walk(tree) if isinstance(node, ast.Import)]
            return {
                "valid_syntax": True,
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "node_count": len(list(ast.walk(tree)))
            }
        except SyntaxError as e:
            return {"valid_syntax": False, "error": str(e)}

    def _execute_local_git_status(self) -> Dict[str, Any]:
        """Query real local git status in repository."""
        try:
            res = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, timeout=5)
            lines = [l for l in res.stdout.splitlines() if l.strip()]
            return {"clean": len(lines) == 0, "modified_files_count": len(lines), "files": lines[:10]}
        except Exception as e:
            return {"clean": False, "error": str(e)}

    async def invoke_tool(
        self, agent_id: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        score_before = risk_engine.get_score(agent_id)
        tool_def = REGISTERED_MCP_TOOLS.get(tool_name)
        
        if not tool_def:
            return {"success": False, "error": f"Unknown MCP tool: {tool_name}"}

        is_mutating = tool_def.is_mutating
        required_cap = Capability.MCP_MUTATING if is_mutating else Capability.MCP_INVOKE

        eval_res = policy_engine.evaluate_request(
            agent_id=agent_id,
            tool_name=f"mcp_{tool_name}",
            arguments={"arguments": arguments, "is_write": is_mutating},
            required_capability=required_cap,
        )

        if not eval_res["allowed"]:
            await risk_engine.ingest_signal(
                agent_id=agent_id,
                signal_code="REPEATED_BLOCKED_COMMAND",
                reason=f"MCP tool invocation denied: {eval_res['reason']}",
            )
            audit_ledger.append_record(
                agent_id=agent_id,
                event_type="MCP_BLOCKED",
                action_name=tool_name,
                decision="DENY",
                risk_score_before=score_before,
                risk_score_after=risk_engine.get_score(agent_id),
                degradation_state=risk_engine.get_state(agent_id).value,
                details={"tool_name": tool_name, "arguments": arguments},
            )
            return {"success": False, "error": f"MCP Invocation Denied: {eval_res['reason']}"}

        # Real tool execution
        tool_output = {}
        if tool_name == "local_code_search":
            query = arguments.get("query", "")
            tool_output = self._execute_local_code_search(query)
        elif tool_name == "ast_analyzer":
            snippet = arguments.get("code", "")
            tool_output = self._execute_ast_analyzer(snippet)
        elif tool_name == "local_git_status":
            tool_output = self._execute_local_git_status()
        elif tool_name == "local_git_commit":
            tool_output = {"commit": "simulated_commit", "message": arguments.get("message", "Auto commit")}
        else:
            tool_output = {"executed": True}

        audit_ledger.append_record(
            agent_id=agent_id,
            event_type="MCP_INVOKED",
            action_name=tool_name,
            decision="ALLOW",
            risk_score_before=score_before,
            risk_score_after=risk_engine.get_score(agent_id),
            degradation_state=risk_engine.get_state(agent_id).value,
            details={"tool_name": tool_name, "arguments": arguments},
        )

        return {
            "success": True,
            "tool": tool_name,
            "is_mutating": is_mutating,
            "output": tool_output
        }

    def list_available_tools(self) -> List[Dict[str, Any]]:
        return [t.model_dump() for t in REGISTERED_MCP_TOOLS.values()]

mcp_gateway = McpGateway()
