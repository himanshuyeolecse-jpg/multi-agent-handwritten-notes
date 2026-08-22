# test_system.py
import pytest
from nodes import critic_node
from graph import check_approval

# 1. Test Node Logic (Using mock inputs)
def test_critic_node_approval():
    fake_state = {
        "summary_notes": "Here are 3 key study notes about AI agents.",
        "image_path": "output_screenshots/handwritten_notes.png", # Assume file exists
        "messages": [],
        "iterations": 0,
        "is_approved": False
    }
    
    # Run the critic node directly
    result = critic_node(fake_state)
    
    # Assert expected state outputs
    assert result["is_approved"] is True
    assert "APPROVED" in result["messages"][0]

# 2. Test Conditional Edge / Loop Guardrail
def test_check_approval_max_iterations():
    # Test that the system stops when reaching max iterations (2)
    max_iter_state = {"is_approved": False, "iterations": 2}
    routing_result = check_approval(max_iter_state)
    
    assert routing_result == "__end__"  # LangGraph END constant
    