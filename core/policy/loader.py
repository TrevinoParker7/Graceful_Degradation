"""
Policy YAML Loader
"""

from pathlib import Path
from typing import Dict, List, Optional
import yaml
from config.settings import config
from .rules import PolicyRule, PolicySet, PolicyDecision

class PolicyLoader:
    def __init__(self, policies_dir: Optional[Path] = None):
        self.policies_dir = policies_dir or config.policies_dir
        self.policies_dir.mkdir(parents=True, exist_ok=True)

    def load_policy_file(self, file_path: Path) -> PolicySet:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            
        rules = []
        for r in data.get("rules", []):
            decision_str = r.get("decision", "DENY").upper()
            decision = getattr(PolicyDecision, decision_str, PolicyDecision.DENY)
            rules.append(
                PolicyRule(
                    rule_id=r.get("rule_id", "rule_anon"),
                    name=r.get("name", "Unnamed Rule"),
                    description=r.get("description", ""),
                    tool_pattern=r.get("tool_pattern", "*"),
                    condition=r.get("condition"),
                    decision=decision,
                    risk_delta=float(r.get("risk_delta", 0.0)),
                    reason=r.get("reason", "Policy rule evaluation"),
                    tags=r.get("tags", []),
                )
            )

        return PolicySet(
            policy_name=data.get("policy_name", file_path.stem),
            version=str(data.get("version", "1.0")),
            description=data.get("description", ""),
            rules=rules,
        )

    def load_all_policies(self) -> Dict[str, PolicySet]:
        policies = {}
        for yaml_path in self.policies_dir.glob("*.yaml"):
            try:
                pset = self.load_policy_file(yaml_path)
                policies[pset.policy_name] = pset
            except Exception as e:
                print(f"Warning: Failed to load policy {yaml_path}: {e}")
        return policies

policy_loader = PolicyLoader()
