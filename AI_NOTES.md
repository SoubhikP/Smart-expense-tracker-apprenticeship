# AI Usage Notes

## 1\. Which parts were AI-generated vs. written by me

\- Written/changed by me: I reviewed every file Claude generated line by line to understand what each part did before using it. I customized the welcome message in the root `/` route in src/main.py to make it sound more natural. I chose FastAPI over Flask (Claude explained the trade-offs) because the free Swagger docs at /docs made manual testing much easier for someone new to APIs like me.

## 2\. What I validated, tested, or changed, and why

\- I set up a virtual environment, installed dependencies, and ran the server locally with `uvicorn src.main:app --reload`.

\- I manually tested every endpoint using the Swagger UI (/docs): added expenses, viewed the full list, filtered by category ("Food"), checked totals (both overall and category-specific — verified the math was correct, e.g. 50+50=100), and deleted an expense — then confirmed via GET /expenses that it was actually removed.

\- I ran `pytest` on a clean checkout and all 11 tests passed.

\- I checked what happens with invalid input (negative amount) and confirmed the API correctly rejects it with a 422 validation error, since Pydantic requires amount > 0.

## 3\. AI suggestions I decided not to use, and why

\- I considered adding the Docker bonus but decided to skip it and instead spend my time thoroughly testing the core required features (add, view, filter, totals, delete) end-to-end, since getting those fully correct and verified mattered more than adding an extra feature.

\- Claude generated case-insensitive category filtering by default; I kept this behavior since it made testing easier and seemed more forgiving for real usage.

\------



