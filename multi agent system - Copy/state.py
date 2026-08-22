from typing import Annotated, Sequence, TypedDict, Any
import operator

class AgentState(TypedDict):
    messages: Annotated[Sequence[Any], operator.add]
    summary_notes: str
    html_content: str
    image_path: str
    iterations: int
    is_approved: bool