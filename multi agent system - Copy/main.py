# main.py
import sys
import os
import traceback
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # Optional dependency; continue if not installed
    def load_dotenv(*args, **kwargs):
        return None
# Avoid requiring the `langchain` package for simple Local runs; use plain dict messages

# load_dotenv() already called above if available

from graph import app

if __name__ == "__main__":
    print("🚀 Starting Multi-Agent Handwritten Notes System...\n")
    
    # Use a simple dict message compatible with `get_message_content` in `nodes.py`
    initial_input = {
        "messages": [{"content": "Explain key concepts of Multi-Agent Systems in AI."}],
        "summary_notes": "",
        "html_content": "",
        "image_path": "",
        "iterations": 0,
        "is_approved": False
    }

    try:
        for output in app.stream(initial_input):
            for node_name, state_update in output.items():
                print(f"=== Completed Node: [{node_name}] ===")
                if "summary_notes" in state_update and state_update["summary_notes"]:
                    print(f"Notes Generated ({len(state_update['summary_notes'])} chars)")
                if "image_path" in state_update and state_update["image_path"]:
                    print(f"📸 Screenshot saved to: {state_update['image_path']}")
                print("-" * 40)

        print("\n✅ Execution Complete!")
        
    except Exception as e:
        print(f"\n❌ Error during graph execution:")
        traceback.print_exc()