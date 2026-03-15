# **Product Requirements Document (PRD): Lumen UI Navigator**

**Status:** Draft / v1.0

## **1\. Executive Summary**

Lumen is a "Large Action Model" (LAM) framework designed to interpret visual user interfaces and execute complex tasks based on natural language intent. Unlike traditional scrapers that rely solely on DOM structures, Lumen uses computer vision and semantic reasoning to interact with web and desktop applications as a human would.

## **2\. Problem Statement**

* **API Gaps:** Many legacy or complex web applications lack public APIs, making automation impossible.  
* **Brittle Automation:** Current RPA (Robotic Process Automation) tools break when a CSS class name changes.  
* **Accessibility Barriers:** Users with motor impairments struggle with complex, non-standard UI layouts.  
* **Testing Overhead:** QA teams spend significant time manually verifying visual states across different screen resolutions.

## **3\. Goals & Objectives**

* **Visual Fidelity:** Achieve 95% accuracy in identifying interactive elements from screenshots alone.  
* **Intent-to-Action:** Correctly decompose high-level prompts (e.g., "Book the cheapest room") into a sequence of low-level actions (click, type, scroll).  
* **Universal Compatibility:** Work across any website or Electron-based application without custom per-site logic.

## **4\. Target Personas**

1. **The Automation Engineer:** Needs to automate workflows across tools that don't have APIs.  
2. **The QA Specialist:** Wants to write "human-like" test cases (e.g., "Ensure the checkout flow works").  
3. **The Power User:** Wants a "Co-pilot" for the web that can perform tedious data entry or research tasks.

## **5\. Functional Requirements (FR)**

### **FR1: Perception (Vision Layer)**

* **Screen Capture:** Capture high-resolution snapshots of the active viewport.  
* **Set-of-Mark (SoM) Labeling:** Automatically identify interactive nodes (buttons, inputs) and overlay unique numerical identifiers.  
* **OCR & Icon Recognition:** Convert text in images to strings and recognize standard iconography (e.g., hamburger menus, gear icons).

### **FR2: Reasoning (The Brain)**

* **Multi-Step Planning:** Deconstruct a user goal into a DAG (Directed Acyclic Graph) of sub-tasks.  
* **Self-Correction:** If an action fails (e.g., a "Submit" button didn't trigger a change), the system must re-evaluate and try an alternative path.  
* **Memory Context:** Maintain a "short-term memory" of recent actions and page states to avoid loops.

### **FR3: Execution (The Hand)**

* **Input Simulation:** Perform hardware-level or browser-level events (Click, Double Click, Drag-and-Drop, Type).  
* **Delay Modeling:** Introduce human-like variable delays to avoid bot detection systems.

## **6\. Technical Architecture**

The Lumen architecture follows a closed-loop "Perceive-Plan-Act" cycle, utilizing a Multi-modal Large Language Model (MLLM) as the central orchestrator.

### **6.1. Perception Pipeline (The Eye)**

1. **Viewport Capture:** The system captures the current application state as a raw RGB image.  
2. **Interactive Element Extraction:** A lightweight script extracts coordinate data for all clickable, typeable, or scrollable elements.  
3. **Set-of-Mark (SoM) Generation:** The raw image and coordinate data are merged to create an annotated screenshot where every interactive element is labeled with a visible numeric ID.  
4. **Semantic Enrichment:** Elements are optionally tagged with metadata (e.g., "ARIA labels") to provide additional context to the VLM.

### **6.2. The Reasoning Engine (The Brain)**

1. **Context Assembly:** The current annotated image, the user’s goal, and the action history are bundled into a prompt.  
2. **VLM Inference:** The model performs visual reasoning to determine which element ID corresponds to the next logical step toward the goal.  
3. **Structured Output:** The model returns a JSON-formatted action object: {"element\_id": 14, "action": "click", "reasoning": "Need to open the search bar first"}.

### **6.3. The Execution Layer (The Hand)**

1. **Coordinate Mapping:** The system translates the element ID back to precise ![][image1] screen coordinates.  
2. **Event Injection:** Using a driver (e.g., Playwright or a Native OS Accessibility API), the physical event is simulated.  
3. **Verification Loop:** A new screenshot is immediately taken to verify the expected state change occurred.

## **7\. Technical Constraints**

* **Model:** Powered by Multi-modal LLMs (e.g., Gemini 2.5 Flash / GPT-4o).  
* **Latency Target:** Each "Reasoning loop" (Screenshot \-\> Action) should take \< 2.5 seconds.  
* **Privacy:** Optional "Local-only" mode for processing sensitive enterprise screenshots.

## **8\. User Flow**

1. **Input:** User types: "Go to Amazon and find me a ergonomic keyboard under $50 with at least 4 stars."  
2. **Perception:** Lumen captures the current browser state.  
3. **Planning:** Lumen identifies the search bar, types the query, and hits Enter.  
4. **Observation:** Lumen "sees" the results page, identifies the "Filters" section, and selects the star rating and price range.  
5. **Completion:** Lumen presents the best option to the user and asks for confirmation to proceed to checkout.

## **9\. Non-Functional Requirements**

* **Reliability:** 99.9% uptime for the reasoning engine.  
* **Security:** Masking of PII (Personally Identifiable Information) in screenshots before sending to cloud inference.  
* **Scalability:** Ability to run multiple "Agents" in headless environments.

## **10\. Success Metrics**

* **Task Completion Rate (TCR):** Percentage of user prompts successfully completed without manual intervention.  
* **Average Steps to Goal:** A measure of the agent's efficiency.  
* **Human-in-the-loop Frequency:** How often the agent needs to ask the user for clarification.

[image1]: <data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAC0AAAAYCAYAAABurXSEAAAEbklEQVR4Xp1XW6iUVRSe4UzgFQ3PODiXvf89Aw6RkDIgiRY+pCim4osER3xIzCcj6KgoBuelh6IyRKgHQwpExCMIokQEBQqKQnAeqoMSZEjiUyAa+GD1rX2ZWfs2c/KDdf7Z67a/vfba+/9PqTQM5VCRx1BXbbQe/iONoUYPvmcujs8fIUcoUowA959rbLVaXVQUxbxsQI5chITj6CA7v5rHddkwMhSqWC2EONNut5eEdsIgOEHIIqHSiGIjGL0qlASmlVLStyTQaDSacP4BpF/WiohXORPMtVFQHjlXKFqt1mtSiEumeJFHH2WQ/RxtMRWo/WEIPrH9k1iC9ysepRTgI+UpcDoSGvrAylbBaZaeoW0o4sk8cNLpxSRgjdj1dZBfIYrr+6AVwXhFH8AAoW+MXNvMBfmloD1eBKfbkAnPQCCiRBhyLLQ51Ov1Fhb2Jj1pjP5fhp3ZipgVoS9H2B69Xu8FpdTryNXDcKxvpnYASa1j3JH/NORsOawMTQy5h5VtdzpmL6uieA8Jv4Dshd8vUsiP8fwG48P4fRckugN3FxX/pkNFBCCTgvJIuc+ZUbiNGP8FWceDbAdc63a7i43eglYtpXgI0hs8g7FtwgTH3TqR/GskuQ95SZrdeWKrNhKIPQD/iWaz1cDz90LRoTfkMP4QHO7XcYM5f7Ig93Zd0P6O2grQpJA/+OSuUNC9iwqtpN+1Wm0hgr+HTGNYwSLXY+Kd8ObbzGCzmEcFi/8AO7MC5N9Cjr9dVQftKaIzZUk/wFxtrvdJ8221YAtoY+IHtGX+/ie6IZHHogIS5yA33QuM8mpiiTNlST9SSr0SGkBaepXW8Aqlr8UdSPBUSNZGeXIlMobmZrOpW4PawemkOdDPMP8b3JdgSItke9BK/6TggbtGGQFvw/4lfQ/AfpImpInJ2Ol0lmMBJ3CjLHAB2N6lJIMUPqgwyPGEH3pB/Sz0DpoWYFsF3wnIb6h0zatAvVEfB7mfFQ6K05GdHCkAMoPfXTx/wgQ/Vseri8gF40OU1MVYn4fSHFTl8nDQNsP2iCpox+Av7kj9jvA/kgjQHzM21uuuAxB4BsaTfUPJ3Kn2trgM+7eQg5IueyGn8bwI21Hycf7222UG8o8jpcGYk7+g65PedEJ+Bd9ZyL8i8boum/6f9m0sGZ1oVPqWMBc8xxi1AVupHec/HZFjPwiFraZBN5AtxlLKA1K7JLtJWGdQlelzj17j9u4O0GjUl8F4vVDFFt/i9iJUcb3XBFSdT2hCriQf6NZgMfQCOU0a+93+HcaXm63mfOM1ABa/B/bzfDcj2NvhAi5/ncDAI8RUaT0m2QL5qMQvjkHltoL0Yzy34TDPx+/P4HuL2qrva2E/E67i23qtb4nndYfrUNIaMEk4VFCd3Z3MPxD25fQp5AbkJm6eg0Q+9KPUWMwUfN7XozwMCdoK3CSTqiheHVjSiPSRIqlKg+0ednwzFv9OX8F/5DMmDAkVxwjzc8DPOIf8eZe8ZRQSJKzq/+b8D2Z53ltaDiHlAAAAAElFTkSuQmCC>
