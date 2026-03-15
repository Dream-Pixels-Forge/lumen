# **Technical Architecture Document: Lumen UI Navigator**

**Version:** 1.0

**Project:** Lumen (Universal Visual Agent)

## **1\. System Overview**

Lumen is designed as a **closed-loop agentic system** that bridges natural language intent and pixel-level execution. The architecture prioritizes "Vision-First" reasoning, allowing it to navigate any graphical user interface (GUI) without requiring underlying metadata or source code access.

## **2\. High-Level Component Diagram**

graph TD  
    User(\[User Prompt\]) \--\> Orchestrator\[Lumen Orchestrator\]  
    Orchestrator \--\> Perception\[Perception Engine\]  
      
    subgraph "Perception Layer"  
        Capture\[Screen Capture Service\]  
        SoM\[Set-of-Mark Annotator\]  
        OCR\[OCR & Icon Classifier\]  
    end  
      
    Perception \--\> Brain\[Reasoning Brain \- MLLM\]  
      
    subgraph "Reasoning Layer"  
        Planner\[Task Planner\]  
        Memory\[Action History & State Log\]  
        Evaluator\[Self-Correction Logic\]  
    end  
      
    Brain \--\> Executor\[Execution Controller\]  
      
    subgraph "Execution Layer"  
        Driver\[Playwright / Native OS Driver\]  
        Verifier\[State Change Verifier\]  
    end  
      
    Executor \--\> App\[Target Application/Website\]  
    App \--\> Perception

## **3\. Core Modules**

### **3.1 Perception Engine (The Eye)**

The Perception Engine transforms raw pixels into a semantically meaningful "Action Map."

* **Visual Grounding:** Uses a Vision Transformer (ViT) to detect interactive regions (buttons, inputs, sliders).  
* **Set-of-Mark (SoM):** Overlays a transparent grid or numbered tags onto the screenshot. This reduces the VLM's coordinate-prediction burden from ![][image1] pixels to simple integer IDs (e.g., "Click button 5").  
* **Context Enrichment:** Extracts text via OCR and maps standard UI icons (e.g., "three lines" ![][image2] "Menu") to provide a text-rich description alongside the image.

### **3.2 Reasoning Brain (The Planner)**

The "Brain" is a Multi-modal Large Language Model (MLLM) that operates in a **ReAct (Reason \+ Act)** loop.

* **Observation:** Interprets the SoM screenshot and current state.  
* **Thought:** Breaks down the high-level goal into the immediate next sub-task.  
* **Action Generation:** Outputs a structured JSON command:  
  {  
    "action": "type",  
    "target\_id": 12,  
    "payload": "mechanical keyboard",  
    "thought": "I need to enter the search query into the identified search bar (ID 12)."  
  }

### **3.3 Execution Controller (The Hand)**

The Controller acts as the bridge to the physical/virtual hardware.

* **Precision Mapping:** Maps the target\_id back to the exact center coordinates of the detected bounding box.  
* **Event Simulation:** Dispatches events (mousedown, keyup, scroll) via drivers like Playwright (Web) or Accessibility APIs (Desktop).  
* **Verification:** After every action, it waits for a "settling time" (to allow animations to finish) and captures a new screenshot to verify if the state has changed as expected.

## **4\. Data Flow (The Action Loop)**

1. **Initialize:** The Orchestrator receives the user prompt and initializes the session state.  
2. **Sense:** Screen Capture Service pulls the current frame.  
3. **Annotate:** SoM Annotator labels interactive elements.  
4. **Reason:** The MLLM receives the image \+ action history \+ user prompt.  
5. **Act:** The Executor performs the chosen action on the target application.  
6. **Reflect:** The Verifier checks the new state. If the goal isn't met, the loop returns to step 2\.

## **5\. Security & Privacy**

* **PII Masking:** Local computer vision models (like YOLO or lightweight ViTs) identify sensitive regions (credit card numbers, names) and redact them before the screenshot is sent to a cloud-based MLLM.  
* **Sandboxing:** The Execution Controller runs in an isolated container to prevent the agent from performing unauthorized system-level commands.

## **6\. Technical Stack**

* **Inference:** Gemini 2.5 Flash / GPT-4o (Vision-capable models).  
* **Backend:** Python (FastAPI) for the Orchestrator.  
* **Drivers:** Playwright (Web), PyAutoGUI (Desktop).  
* **Vision Processing:** OpenCV, PyTorch (for local SoM and Redaction).

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAYCAYAAABurXSEAAAEbklEQVR4Xp1XW6iUVRSe4UzgFQ3PODiXvf89Aw6RkDIgiRY+pCim4osER3xIzCcj6KgoBuelh6IyRKgHQwpExCMIokQEBQqKQnAeqoMSZEjiUyAa+GD1rX2ZWfs2c/KDdf7Z67a/vfba+/9PqTQM5VCRx1BXbbQe/iONoUYPvmcujs8fIUcoUowA959rbLVaXVQUxbxsQI5chITj6CA7v5rHddkwMhSqWC2EONNut5eEdsIgOEHIIqHSiGIjGL0qlASmlVLStyTQaDSacP4BpF/WiohXORPMtVFQHjlXKFqt1mtSiEumeJFHH2WQ/RxtMRWo/WEIPrH9k1iC9ysepRTgI+UpcDoSGvrAylbBaZaeoW0o4sk8cNLpxSRgjdj1dZBfIYrr+6AVwXhFH8AAoW+MXNvMBfmloD1eBKfbkAnPQCCiRBhyLLQ51Ov1Fhb2Jj1pjP5fhp3ZipgVoS9H2B69Xu8FpdTryNXDcKxvpnYASa1j3JH/NORsOawMTQy5h5VtdzpmL6uieA8Jv4Dshd8vUsiP8fwG48P4fRckugN3FxX/pkNFBCCTgvJIuc+ZUbiNGP8FWceDbAdc63a7i43eglYtpXgI0hs8g7FtwgTH3TqR/GskuQ95SZrdeWKrNhKIPQD/iWaz1cDz90LRoTfkMP4QHO7XcYM5f7Ig93Zd0P6O2grQpJA/+OSuUNC9iwqtpN+1Wm0hgr+HTGNYwSLXY+Kd8ObbzGCzmEcFi/8AO7MC5N9Cjr9dVQftKaIzZUk/wFxtrvdJ8221YAtoY+IHtGX+/ie6IZHHogIS5yA33QuM8mpiiTNlST9SSr0SGkBaepXW8Aqlr8UdSPBUSNZGeXIlMobmZrOpW4PawemkOdDPMP8b3JdgSItke9BK/6TggbtGGQFvw/4lfQ/AfpImpInJ2Ol0lmMBJ3CjLHAB2N6lJIMUPqgwyPGEH3pB/Sz0DpoWYFsF3wnIb6h0zatAvVEfB7mfFQ6K05GdHCkAMoPfXTx/wgQ/Vseri8gF40OU1MVYn4fSHFTl8nDQNsP2iCpox+Av7kj9jvA/kgjQHzM21uuuAxB4BsaTfUPJ3Kn2trgM+7eQg5IueyGn8bwI21Hycf7222UG8o8jpcGYk7+g65PedEJ+Bd9ZyL8i8boum/6f9m0sGZ1oVPqWMBc8xxi1AVupHec/HZFjPwiFraZBN5AtxlLKA1K7JLtJWGdQlelzj17j9u4O0GjUl8F4vVDFFt/i9iJUcb3XBFSdT2hCriQf6NZgMfQCOU0a+93+HcaXm63mfOM1ABa/B/bzfDcj2NvhAi5/ncDAI8RUaT0m2QL5qMQvjkHltoL0Yzy34TDPx+/P4HuL2qrva2E/E67i23qtb4nndYfrUNIaMEk4VFCd3Z3MPxD25fQp5AbkJm6eg0Q+9KPUWMwUfN7XozwMCdoK3CSTqiheHVjSiPSRIqlKg+0ednwzFv9OX8F/5DMmDAkVxwjzc8DPOIf8eZe8ZRQSJKzq/+b8D2Z53ltaDiHlAAAAAElFTkSuQmCC>

[image2]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABMAAAAXCAYAAADpwXTaAAABjElEQVR4XoVUvU7DMBBuJCSQ+BESlKpKcueUiD4APAxTRwYmdkbEyIRYujAw8gK8GDtn+y6+sx3xKY7P3/18Z9fpYhHQqJFBKJ7LCM2U3hJZTJHSNFbLL7MmJiSPhWGLjYlCPVeh3LO0xKPwVNCEMNMpq5flK0iKM7BbsSeSbLEUo7vXMlarkacKzQ/OHSHCw3J5eVLNEA0jXAv0oPYQ8BUAbisNzP3wCd6vNrXwhRDxjZYHEjH59R0TLhmFdni7wT0hwC6mSwzNzrlzUlrHAWvaBttxDWGwj/nrzYYo/CTufRzHsyCyWl0dE/FMjj0A7v2Mfg428JpnM4Di4YfsXxovVPBQmlfIT6iOvu/vSPC7bdsuECFNZYSTiw97MzBFBS6om69hGNCEpT7SQgRSnC1MhR6dG+4TI35TTUH7FZy/tIAfXde11pN3kCXGCxPJ8GbzZrs9ZWeRw0zJmvvD8z9fSU7ka0FqRLdko3Ml/8zV05Cqekgx0ZnqZAUtL4rFZ6iW8W90Ftplw2LeH8gsKIi2sfJ3AAAAAElFTkSuQmCC>