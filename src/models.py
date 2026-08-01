"""
Data models for the Expense Tracker API.

We use Pydantic models because FastAPI uses them to:
1. Validate incoming request data automatically (e.g. reject a request
   where "amount" is a string like "abc" instead of a number).
2. Auto-generate the OpenAPI/Swagger documentation.
"""

from datetime import date as date_type
from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """Shape of the data a client sends us when creating a new expense.
    Notice there is no 'id' here — the server assigns that, not the client.
    """
    title: str = Field(..., min_length=1, description="Short description of the expense")
    amount: float = Field(..., gt=0, description="Expense amount, must be greater than 0")
    category: str = Field(..., min_length=1, description="e.g. Food, Travel, Rent")
    date: date_type = Field(..., description="Date of the expense, format YYYY-MM-DD")


class Expense(ExpenseCreate):
    """Shape of an expense once it's stored — same as ExpenseCreate but with an id."""
    id: int
