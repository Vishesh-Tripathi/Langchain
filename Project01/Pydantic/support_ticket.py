from pydantic import BaseModel, Field
from typing import Literal


class SupportTicket(BaseModel):
    category: Literal[
        "Billing",
        "Technical",
        "Account",
        "Delivery",
        "Order",
        "Refund",
        "Other"
    ]

    priority: Literal[
        "High",
        "Medium",
        "Low"
    ]

    sentiment: Literal[
        "Positive",
        "Neutral",
        "Negative"
    ]

    summary: str = Field(
        description="A short description of the customer's problem"
    )

    recommended_team: str = Field(
        description="The support team that should handle the issue"
    )

    requires_human_agent: bool = Field(
        description="Whether the issue requires intervention from a human support agent"
    )