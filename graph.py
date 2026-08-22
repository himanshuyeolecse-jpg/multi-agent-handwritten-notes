from typing import Dict, Any
from nodes import researcher_node, note_renderer_node, critic_node

# Simple END marker consistent with tests
END = "__end__"


def check_approval(state: Dict[str, Any]):
    """Return END if approved or iterations >= 2, else loop back to researcher."""
    if state.get("is_approved") or state.get("iterations", 0) >= 2:
        return END
    return "researcher"


class SimpleApp:
    def __init__(self):
        self.entry = "researcher"

    def stream(self, initial_state: Dict[str, Any]):
        state = dict(initial_state)
        # Ensure keys exist
        state.setdefault("messages", [])
        state.setdefault("summary_notes", "")
        state.setdefault("html_content", "")
        state.setdefault("image_path", "")
        state.setdefault("iterations", 0)
        state.setdefault("is_approved", False)

        while True:
            # researcher
            res = researcher_node(state)
            state.update(res)
            yield {"researcher": res}

            # note renderer
            res = note_renderer_node(state)
            state.update(res)
            yield {"note_renderer": res}

            # critic
            res = critic_node(state)
            state.update(res)
            yield {"critic": res}

            # decide next
            route = check_approval(state)
            if route == END:
                break
            state["iterations"] = state.get("iterations", 0) + 1


app = SimpleApp()