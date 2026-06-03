from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class TraceStep:
    step: int
    thought: str = ""
    action: Optional[str] = None
    action_input: Dict[str, Any] = field(default_factory=dict)
    observation: Optional[str] = None
    final_answer: Optional[str] = None
    raw_output: str = ""
    error: Optional[str] = None