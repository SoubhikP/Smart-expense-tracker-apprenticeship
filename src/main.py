"""
Smart Expense Tracker API
==========================

A small REST API to add, view, filter, total, and delete personal expenses.

Run it with (from the project root):
    uvicorn src.main:app --reload

Then open http://127.0.0.1:8000/docs for interactive Swagger documentation
(this comes free with FastAPI - it's the "OpenAPI/Swagger docs" bonus item).
"""

from typing import List, Optional

from fastapi import FastAPI, HTTPException, Query

from src import storage
from src.models import Expense, ExpenseCreate

app = FastAPI(
    title="Smart Expense Tracker API",
    description="A simple REST API to manage personal expenses.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    """Basic health check / welcome route."""
    return {"message": "Smart Expense Tracker API is running. Visit /docs for API docs."}


@app.post("/expenses", response_model=Expense, status_code=201, tags=["Expenses"])
def add_expense(expense: ExpenseCreate):
    """Add a new expense. The server assigns the id automatically."""
    new_expense = expense.model_dump()
    new_expense["id"] = storage.next_id()
    # Convert date object to string so it can be saved to JSON safely.
    new_expense["date"] = str(new_expense["date"])
    saved = storage.add(new_expense)
    return saved


@app.get("/expenses", response_model=List[Expense], tags=["Expenses"])
def get_expenses(
    category: Optional[str] = Query(
        None, description="Filter expenses by category, e.g. ?category=Food"
    )
):
    """View all expenses, or filter by category using a query parameter."""
    expenses = storage.get_all()
    if category:
        expenses = [e for e in expenses if e["category"].lower() == category.lower()]
    return expenses


@app.get("/expenses/total", tags=["Expenses"])
def get_total(
    category: Optional[str] = Query(
        None, description="If provided, total only this category. Otherwise, totals everything."
    )
):
    """
    Calculate total expenses.
    - No query param -> overall total AND a breakdown by category.
    - ?category=Food -> total for just that category.
    """
    expenses = storage.get_all()

    if category:
        filtered = [e for e in expenses if e["category"].lower() == category.lower()]
        total = round(sum(e["amount"] for e in filtered), 2)
        return {"category": category, "total": total}

    overall_total = round(sum(e["amount"] for e in expenses), 2)
    by_category = {}
    for e in expenses:
        by_category[e["category"]] = round(by_category.get(e["category"], 0) + e["amount"], 2)

    return {"overall_total": overall_total, "by_category": by_category}


@app.delete("/expenses/{expense_id}", status_code=200, tags=["Expenses"])
def delete_expense(expense_id: int):
    """Delete an expense by its id. Returns 404 if the id doesn't exist."""
    deleted = storage.delete(expense_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Expense with id {expense_id} not found")
    return {"message": f"Expense {expense_id} deleted successfully"}
