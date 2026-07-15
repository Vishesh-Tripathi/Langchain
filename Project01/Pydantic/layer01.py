from pydantic import BaseModel
from typing import Literal

class QueryAnalysis(BaseModel):
    topic: str
    problem_details: str
    intent: str
    required_action: Literal[
        "direct_answer",
        "tool_required",
        "support_issue"
    ]