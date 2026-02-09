from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict

import google.generativeai as genai

from config import configure_gemini, MODEL_STRICT
from utils.retry import with_retries

try:
    from prompts.analyzer_prompt import ANALYZER_SYSTEM_PROMPT
except Exception:
    ANALYZER_SYSTEM_PROMPT = "You are an expert analyzer. Return ONLY JSON."

logger = logging.getLogger(__name__)


def analyze_paper(pdf_path: str) -> Dict[str, Any]:
    """Analyze a PDF and return structured JSON text + optional parsed dict.

    Returns:
        {
          "success": bool,
          "data": {"raw": str, "parsed": dict | None} | None,
          "error": str
        }
    """
    try:
        if not os.path.exists(pdf_path) or not pdf_path.lower().endswith(".pdf"):
            raise ValueError(f"PDF not found or not a .pdf: {pdf_path}")

        configure_gemini()
        model = genai.GenerativeModel(
            model_name=MODEL_STRICT,
            system_instruction=ANALYZER_SYSTEM_PROMPT,
        )

        uploaded = genai.upload_file(
            pdf_path,
            mime_type="application/pdf",
            display_name=os.path.basename(pdf_path),
        )

        resp = with_retries(lambda: model.generate_content(
            [uploaded, "Extract concepts per schema and return ONLY JSON."]
        ))
        raw = resp.text or ""
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            logger.debug("Analyzer JSON parse failed; returning raw only")

        return {"success": True, "data": {"raw": raw, "parsed": parsed}, "error": ""}

    except Exception as e:
        logger.exception("Analyzer failed")
        return {"success": False, "data": None, "error": str(e)}
"""
from __future__ import annotations

import json
import logging
from typing import Any, Dict

import google.generativeai as genai

from config import configure_gemini, MODEL_FAST, MODEL_STRICT
# Prefer the stricter model for analysis
try:
    from prompts.analyzer_prompt import ANALYZER_SYSTEM_PROMPT
except Exception:
    ANALYZER_SYSTEM_PROMPT = "You are an expert analyzer. Return ONLY JSON."

from utils.retry import with_retries

logger = logging.getLogger(__name__)


def analyze_paper(pdf_path: str) -> Dict[str, Any]:
    ###Analyze a PDF, returning analyzer JSON (as text) plus optional parsed dict.

    ###Returns:
        {"success": bool, "data": {"raw": str, "parsed": dict|None}, "error": str}
    
    try:
        configure_gemini()
        model = genai.GenerativeModel(
            model_name=MODEL_STRICT,
            system_instruction=ANALYZER_SYSTEM_PROMPT,
        )
        uploaded = genai.upload_file(pdf_path)
        resp = with_retries(lambda: model.generate_content(
            [uploaded, "Extract concepts per schema and return ONLY JSON."]
        ))
        raw = resp.text or ""
        parsed = None
        try:
            parsed = json.loads(raw)
        except Exception:
            # Keep going; downstream can still use raw text
            logger.debug("Analyzer JSON parse failed; returning raw only")

        return {"success": True, "data": {"raw": raw, "parsed": parsed}, "error": ""}
    except Exception as e:
        logger.exception("Analyzer failed")
        return {"success": False, "data": None, "error": str(e)}
"""