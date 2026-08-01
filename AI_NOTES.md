# AI Usage Notes

## 1. Which parts were AI-generated vs. written by me

I used Claude (Anthropic) as my primary coding assistant for this
assignment, since I'm early in my learning journey with backend
development. Here's the honest breakdown:

- **AI-generated**: the overall project structure, the FastAPI routes in
  `src/main.py`, the Pydantic models in `src/models.py`, the JSON-file
  storage layer in `src/storage.py`, and the pytest test suite in
  `tests/test_expenses.py`.
- **Written/decided by me**: [FILL IN — e.g. "I chose FastAPI over Flask
  after asking Claude to compare them, because the free Swagger docs
  seemed useful for a review process like this one." / any endpoint
  names, field names, or behavior I specifically asked to be changed /
  any bug I found and asked to be fixed.]

I chose to be upfront about this rather than pretend otherwise, since the
assignment explicitly says AI use is expected and normal — what matters
is how it was used and verified.

## 2. What I validated, tested, or changed, and why

- [FILL IN — describe running `pytest` yourself on a clean checkout, and
  whether all tests passed. Example: "I ran `pytest` after cloning to a
  fresh folder and all 10 tests passed."]
- [FILL IN — describe manually testing the API, e.g. using the `/docs`
  Swagger UI or `curl`, to add an expense, filter by category, check the
  total, and delete an expense — and confirm the responses matched what
  was expected.]
- [FILL IN — any edge case you specifically checked, e.g. "I tested
  adding an expense with a negative amount and confirmed the API
  correctly rejects it with a 422 error, since `amount` is required to
  be greater than 0."]
- [FILL IN — any change you made to AI-generated code after reviewing it,
  even something small, e.g. renaming a variable, adjusting an error
  message, or changing the JSON file name.]

## 3. AI suggestions I decided not to use, and why

- [FILL IN — e.g. "Claude initially suggested storing dates as full
  datetime objects instead of plain dates; I kept it simple as just a
  date since the assignment only asks for a 'date' field."]
- [FILL IN — if you asked for the Docker bonus or search bonus and
  decided not to include it, note that here and why — e.g. "I considered
  the Docker bonus but skipped it to make sure the core requirements
  were solid and well-tested within the time I had."]

---
**Note to self before submitting**: replace every `[FILL IN ...]` above
with what actually happened when I ran and tested this on my own machine.
This file is explicitly part of the evaluation, so it needs to reflect
my real process, not a generic placeholder.
