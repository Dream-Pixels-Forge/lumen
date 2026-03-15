# Lumen Initialization Plan

## 1. Project Structure
Based on the `Lumen Technical Architecture.md`, we will structure the project as follows:

```
lumen/
├── backend/                # Orchestrator (FastAPI)
│   ├── app/
│   │   ├── main.py         # Entry point
│   │   ├── api/            # API Routes
│   │   └── core/           # Config & Events
├── perception/             # Vision Layer
│   ├── som/                # Set-of-Mark Annotator
│   └── ocr/                # OCR & Icon Recognition
├── reasoning/              # Brain Layer
│   ├── planner/            # Task Planner
│   └── llm/                # Model Interfaces (Gemini/GPT)
├── execution/              # Action Layer
│   ├── web/                # Playwright Driver
│   └── desktop/            # PyAutoGUI Driver (Placeholder)
├── tests/                  # Test Suite
├── docs/                   # Documentation
├── .gitignore
├── README.md
└── requirements.txt        # Python Dependencies
```

## 2. Core Dependencies
- **Framework:** FastAPI, Uvicorn
- **Vision:** Opencv-python, Pillow, Torch (lightweight if possible), Ultralytics (YOLO/SoM)
- **Automation:** Playwright, PyAutoGUI
- **LLM:** Google-GenerativeAI (Gemini), OpenAI

## 3. Action Items (Sprint 0: Init)
1.  **Repository Setup:** Initialize Git and `.gitignore`.
2.  **Scaffold Structure:** Create folders and `__init__.py` files.
3.  **Environment Setup:** Create `requirements.txt`.
4.  **Backend Skeleton:** Create basic FastAPI health check endpoint.
5.  **Documentation:** Update README with setup instructions.
