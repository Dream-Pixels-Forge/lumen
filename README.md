# Lumen UI Navigator

A "Large Action Model" (LAM) framework designed to interpret visual user interfaces and execute complex tasks based on natural language intent.

## Architecture

Lumen follows a closed-loop "Perceive-Plan-Act" cycle:
1.  **Perception (The Eye):** Uses Computer Vision (SoM) to understand the UI.
2.  **Reasoning (The Brain):** Uses MLLMs (Gemini/GPT-4o) to plan actions.
3.  **Execution (The Hand):** Uses Playwright/PyAutoGUI to interact with the system.

## Project Structure

- `backend/`: FastAPI Orchestrator
- `perception/`: Vision modules (SoM, OCR)
- `reasoning/`: Task planner and LLM integration
- `execution/`: Driver implementations
- `tests/`: Pytest suite

## Getting Started

### Prerequisites

- Python 3.10+
- Playwright (for web automation)

### Installation

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

### Running the Server

```bash
uvicorn backend.app.main:app --reload
```

### Running Tests

```bash
pytest
```
