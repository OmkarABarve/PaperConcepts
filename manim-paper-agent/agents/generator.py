from __future__ import annotations

import json
import logging
from typing import Any, Dict, Union

import google.generativeai as genai

from config import configure_gemini, MODEL_FAST

try:
    from prompts.generator_prompt import SCRIPT_GENERATOR_SYSTEM_PROMPT
except Exception:
    SCRIPT_GENERATOR_SYSTEM_PROMPT = "You are a director. Return ONLY JSON storyboard."

from utils.retry import with_retries

logger = logging.getLogger(__name__)


def generate_directed_script(analyzer_output: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Turn analyzer output into a directed script JSON for the code-writer.

    Args:
        analyzer_output: Analyzer JSON as a string, or parsed dict.

    Returns:
        {"success": bool, "data": {"raw": str, "parsed": dict|None}, "error": str}
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel(
            model_name=MODEL_FAST,
            system_instruction=SCRIPT_GENERATOR_SYSTEM_PROMPT,
            generation_config={"response_mime_type": "application/json"},
        )

        if isinstance(analyzer_output, dict):
            analyzer_text = json.dumps(analyzer_output)
        else:
            analyzer_text = analyzer_output

        resp = with_retries(lambda: model.generate_content(
            [analyzer_text, "Produce the directed script as STRICT JSON only."]
        ))
        raw = (resp.text or "").strip()

# Strip common markdown code fences like 
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            logger.debug("Generator JSON parse failed; returning raw only")

        return {"success": True, "data": {"raw": raw, "parsed": parsed}, "error": ""}
    except Exception as e:
        logger.exception("Script generator failed")
        return {"success": False, "data": None, "error": str(e)}