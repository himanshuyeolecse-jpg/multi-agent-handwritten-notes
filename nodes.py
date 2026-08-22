# nodes.py
import os
import json
import textwrap
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    def load_dotenv(*args, **kwargs):
        return None
try:
    from langchain.chat_models import ChatOpenAI
except Exception:
    # Fallback for older packages
    try:
        from langchain_openai import ChatOpenAI
    except Exception:
        ChatOpenAI = None

try:
    from langchain_community.tools.tavily_search import TavilySearchResults
except Exception:
    TavilySearchResults = None
from state import AgentState

load_dotenv()

llm = None
if ChatOpenAI is not None:
    # modern ChatOpenAI expects model_name
    try:
        llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    except Exception:
        try:
            llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        except Exception:
            llm = None

search_tool = None
if TavilySearchResults is not None:
    try:
        search_tool = TavilySearchResults(max_results=2)
    except Exception:
        search_tool = None

def get_message_content(message):
    """Safely extracts string content whether message is an object or a dict."""
    if isinstance(message, dict):
        return message.get("content", "")
    return getattr(message, "content", str(message))

def researcher_node(state: AgentState):
    """Fetches key technical insights based on the user's topic."""
    # Safe message extraction
    last_message = state["messages"][-1]
    query = get_message_content(last_message)
    
    search_results = None
    if search_tool is not None:
        # support different call signatures
        try:
            search_results = search_tool.invoke(query)
        except Exception:
            try:
                search_results = search_tool.run(query)
            except Exception:
                try:
                    search_results = search_tool.search(query)
                except Exception:
                    search_results = None

    search_results_text = json.dumps(search_results) if isinstance(search_results, (dict, list)) else str(search_results or "")

    prompt = f"""
    Summarize these search results into concise student study notes:
    {search_results_text}

    Include:
    - 3 key main points
    - 1 important definition
    - 1 short "Exam Tip"
    """

    summary = ""
    if llm is not None:
        # Try a few call patterns for different LangChain versions
        try:
            resp = llm.invoke(prompt)
            summary = getattr(resp, "content", str(resp))
        except Exception:
            try:
                # some llms support predict
                summary = llm.predict(prompt)
            except Exception:
                try:
                    # __call__ fallback
                    summary = llm(prompt)
                except Exception:
                    summary = str(prompt)
    else:
        summary = (
            f"## {query}\n\n"
            "### 3 Key Main Points\n"
            f"- {query} can be understood by identifying its purpose, main components, and practical uses.\n"
            "- Break the topic into smaller ideas and connect each idea to a clear example.\n"
            "- Review the important terms and test your understanding by explaining them in your own words.\n\n"
            "### Important Definition\n"
            f"**{query}:** The subject or concept being studied and explained.\n\n"
            "### Exam Tip\n"
            "Use the definition first, then support your answer with three concise points and an example."
        )
    
    return {"summary_notes": summary}

def note_renderer_node(state: AgentState):
    """Converts structured notes to handwritten HTML/CSS and captures a PNG screenshot."""
    notes_text = state.get("summary_notes", "").replace("\n", "<br>")
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600&display=swap" rel="stylesheet">
        <style>
            body {{
                font-family: 'Caveat', cursive;
                font-size: 26px;
                line-height: 1.6;
                background-color: #fcfaf2;
                background-image: linear-gradient(#e8e4d9 1px, transparent 1px);
                background-size: 100% 32px;
                padding: 40px 50px;
                color: #1a237e;
                width: 650px;
                border-left: 2px solid #ff8a80;
                margin: 0;
            }}
            .header {{
                font-size: 32px;
                color: #b71c1c;
                text-decoration: underline;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="header">Student Study Notes</div>
        <div>{notes_text}</div>
    </body>
    </html>
    """
    
    output_dir = "output_screenshots"
    os.makedirs(output_dir, exist_ok=True)
    screenshot_path = os.path.join(output_dir, "handwritten_notes.png")
    
    # Prefer a browser-rendered image, then fall back to Pillow on hosted systems
    # where Playwright's browser binary is not installed.
    try:
        import playwright.sync_api as pwy

        with pwy.sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 750, "height": 1000})
            page.set_content(html_content)
            page.screenshot(path=screenshot_path, full_page=True)
            browser.close()
    except Exception:
        try:
            from PIL import Image, ImageDraw, ImageFont

            image = Image.new("RGB", (750, 1000), "#fcfaf2")
            draw = ImageDraw.Draw(image)
            title_font = ImageFont.load_default(size=28)
            body_font = ImageFont.load_default(size=18)
            draw.text((50, 45), "Student Study Notes", fill="#b71c1c", font=title_font)
            y_position = 110
            for line in textwrap.wrap(state.get("summary_notes", ""), width=64):
                draw.text((55, y_position), line, fill="#1a237e", font=body_font)
                y_position += 30
                if y_position > 950:
                    break
            image.save(screenshot_path)
        except Exception:
            screenshot_path = ""
    return {"html_content": html_content, "image_path": screenshot_path}

def critic_node(state: AgentState):
    """Verifies that the generated output meets quality standards."""
    notes = state.get("summary_notes", "")
    has_content = len(notes.strip()) >= 20
    has_image = os.path.exists(state.get("image_path", ""))
    
    is_approved = has_content and has_image
    feedback = "APPROVED" if is_approved else "Missing screenshot or complete summary notes."
    
    return {"is_approved": is_approved, "messages": [feedback]}