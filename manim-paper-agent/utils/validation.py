from __future__ import annotations

from typing import Any, Dict, List, Set
from jsonschema import Draft202012Validator

ALLOWED_POSITIONS: Set[str] = {
    "CENTER", "TOP", "BOTTOM", "LEFT", "RIGHT",
    "TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT",
}

ALLOWED_COLORS: Set[str] = {
    "WHITE", "YELLOW", "BLUE", "GREEN", "RED", "ORANGE", "PURPLE", "TEAL",
}

ALLOWED_ACTIONS: Set[str] = {
    "add_text", "add_math", "transform_text", "transform_math",
    "move_to", "highlight", "fade_out", "wait", "add_arrow",
    "add_axes", "add_label", "move_next_to", "add_arrow_id",
    "add_plot", "add_bar_chart", "add_number_line",
}

SCRIPT_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "required": ["video_title", "scenes"],
    "properties": {
        "video_title": {"type": "string"},
        "concept_id": {"type": "string"},
        "duration_sec": {"type": "number"},
        "narration": {"type": "string"},
        "scenes": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "steps"],
                "properties": {
                    "id": {"type": "string"},
                    "scene_duration_sec": {"type": "number"},
                    "steps": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["action"],
                            "properties": {
                                "action": {"type": "string"},
                                "id": {"type": "string"},
                                "at": {"type": "string"},
                                "from_at": {"type": "string"},
                                "to_at": {"type": "string"},
                                "side": {"type": "string"},
                                "color": {"type": "string"},
                                "seconds": {"type": "number"},
                                "run_time": {"type": "number"},
                            },
                        },
                    },
                },
            },
        },
    },
}


def _assert_allowed_tokens(script: Dict[str, Any]) -> None:
    for scene in script.get("scenes", []):
        for step in scene.get("steps", []):
            action = step.get("action", "")
            if action not in ALLOWED_ACTIONS:
                raise ValueError(f"Unsupported action: {action}")
            for key in ("at", "from_at", "to_at"):
                if key in step and step[key] not in ALLOWED_POSITIONS:
                    raise ValueError(f"Invalid position token in '{key}': {step[key]}")
            if "side" in step and step["side"] not in {
                "TOP", "BOTTOM", "LEFT", "RIGHT",
                "TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT",
            }:
                raise ValueError(f"Invalid side token: {step['side']}")
            if "color" in step and step["color"] not in ALLOWED_COLORS:
                raise ValueError(f"Invalid color: {step['color']}")


def _assert_unique_ids(script: Dict[str, Any]) -> None:
    seen: Set[str] = set()
    for scene in script.get("scenes", []):
        for step in scene.get("steps", []):
            # Only enforce uniqueness for creation steps that must define a new id
            if step.get("action") in {"add_text", "add_math", "add_arrow", "add_axes", "add_label", "add_arrow_id", "add_plot", "add_bar_chart", "add_number_line"}:
                sid = step.get("id")
                if not sid:
                    raise ValueError("Creation step missing 'id'")
                if sid in seen:
                    raise ValueError(f"Duplicate object id: {sid}")
                seen.add(sid)


def validate_script(script: Dict[str, Any]) -> None:
    """Validate the directed script JSON against schema and custom rules."""
    Draft202012Validator(SCRIPT_SCHEMA).validate(script)
    _assert_allowed_tokens(script)
    _assert_unique_ids(script)

