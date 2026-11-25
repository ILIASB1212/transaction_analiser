from dataclasses import dataclass
from pydantic_ai import RunContext
from enum import Enum
from pydantic import BaseModel, Field

@dataclass
class CustomerRecords:
    customers: dict

class TransactionCategory(str, Enum):
    groceries = "groceries" 
    dining = "dining" 
    travel = "travel"
    utilities = "utilities"
    entertainment = "entertainment"
    shopping = "shopping"
    other = "other"

class TransactionAnalysis(BaseModel):
    category: TransactionCategory
    amount: float = Field(gt=0)
    fraud_risk_score: int = Field(ge=0, le=100, description="0 = no risk, 100 = certain fraud")
    flagged: bool
    reasoning: str