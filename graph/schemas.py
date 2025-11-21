from typing import TypedDict, List, Dict, Any

class GraphState(TypedDict):
    audio_path: str | None
    transcript: str | None
    intent: Dict[str, Any] | None
    plan: Dict[str, Any] | None
    evidence: Dict[str, List[Dict]] | None
    answer: str | None
    citations: List[Dict] | None
    safety_flags: List[str] | None
    tts_path: str | None
    log: List[Dict] | None
