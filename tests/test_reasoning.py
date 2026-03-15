import pytest
from reasoning.planner.core import VisualPlanner
from unittest.mock import AsyncMock, MagicMock


@pytest.mark.asyncio
async def test_planner_build_prompt():
    mock_llm = MagicMock()
    planner = VisualPlanner(mock_llm)

    goal = "Search for keyboards"
    elements = [{"id": 1, "text": "Search box"}]

    prompt = planner._build_prompt(goal, elements)

    assert "Search for keyboards" in prompt
    assert "Search box" in prompt
    assert "Respond ONLY with a JSON object" in prompt


@pytest.mark.asyncio
async def test_planner_plan_next_step():
    mock_llm = AsyncMock()
    mock_llm.think.return_value = {
        "thought": "I need to click the search box",
        "action": "click",
        "target_id": 1,
        "payload": None,
    }

    planner = VisualPlanner(mock_llm)
    result = await planner.plan_next_step("goal", "path/to/img", [])

    assert result["action"] == "click"
    assert result["target_id"] == 1
