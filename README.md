# Smart Expense Tracker API

A REST API to manage personal expenses — add, view, filter by category,
calculate totals (overall and by category), and delete expenses.

Built with **Python + FastAPI**, storing data in a local JSON file
(`expenses_data.json`, created automatically on first run). No database
required.

## What it does

- `POST /expenses` — add a new expense (title, amount, category, date)
- `GET /expenses` — view all expenses
- `GET /expenses?category=Food` — filter expenses by category
- `GET /expenses/total` — overall total + breakdown by category
- `GET /expenses/total?category=Food` — total for one category
- `DELETE /expenses/{id}` — delete an expense by id

Bonus included: **interactive Swagger/OpenAPI docs**, generated automatically
by FastAPI — once the server is running, open `http://127.0.0.1:8000/docs`
in your browser to try every endpoint from the UI.

## Requirements

- Python 3.10 or newer
- pip

## Installation

Clone the repo, then from the project root:

```bash
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running the server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
Interactive docs: `http://127.0.0.1:8000/docs`

## Running the tests

```bash
pytest
```

This runs the full test suite in `tests/test_expenses.py`, covering:
adding valid/invalid expenses, listing, filtering by category, totals
(overall and per-category), deleting, and deleting a non-existent id.

## Example usage (once the server is running)

```bash
# Add an expense
curl -X POST http://127.0.0.1:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "amount": 45.50, "category": "Food", "date": "2026-01-15"}'

# View all expenses
curl http://127.0.0.1:8000/expenses

# Filter by category
curl "http://127.0.0.1:8000/expenses?category=Food"

# Totals
curl http://127.0.0.1:8000/expenses/total

# Delete an expense
curl -X DELETE http://127.0.0.1:8000/expenses/1
```

## Project structure

```
your-repo/
  README.md
  AI_NOTES.md
  requirements.txt
  src/
    main.py       # FastAPI app + all routes
    models.py      # Pydantic request/response models
    storage.py      # JSON-file storage layer
  tests/
    test_expenses.py
```

## Notes on design decisions

- **Storage**: a JSON file rather than pure in-memory, so data isn't lost
  if the server restarts.
- **IDs**: auto-assigned by the server (max existing id + 1), so clients
  never have to worry about collisions.
- **Validation**: handled by Pydantic — e.g. `amount` must be greater than
  0, and all fields are required. Invalid input returns a `422` response
  with details on what was wrong.
- **Category filtering**: case-insensitive, so `?category=food` and
  `?category=Food` return the same results.
