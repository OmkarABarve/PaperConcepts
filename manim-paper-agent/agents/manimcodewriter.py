from __future__ import annotations

import json
import logging
import os
import re
import subprocess
import sys
from typing import Any, Dict, Union

import google.generativeai as genai

from config import configure_gemini, MODEL_FAST

try:
    from prompts.manime_code_writer import manime_code_writer_prompt
except Exception:
    manime_code_writer_prompt = "You are a Manim code writer. Output ONLY Python code."

from utils.retry import with_retries

logger = logging.getLogger(__name__)


def generate_manim_code(directed_script: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """Use Gemini to turn a directed script JSON into Manim Python code.

    Args:
        directed_script: storyboard JSON (str or dict)

    Returns:
        {"success": bool, "data": {"code": str}, "error": str}
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel(
            model_name=MODEL_FAST,
            system_instruction=manime_code_writer_prompt,
        )

        if isinstance(directed_script, dict):
            script_text = json.dumps(directed_script)
        else:
            script_text = directed_script

        resp = with_retries(lambda: model.generate_content([script_text]))
        code = resp.text or ""
        return {"success": True, "data": {"code": code}, "error": ""}
    except Exception as e:
        logger.exception("Manim code writer failed")
        return {"success": False, "data": None, "error": str(e)}


def write_scene_file(code_text: str, out_dir: str) -> str:
    """Write the generated Manim code to 'scene.py' under out_dir and return its path."""
    os.makedirs(out_dir, exist_ok=True)
    scene_path = os.path.join(out_dir, "scene.py")
    with open(scene_path, "w", encoding="utf-8") as f:
        f.write(code_text)
    return scene_path


def detect_scene_class(code_text: str, default: str = "ExplainerScene") -> str:
    """Detect the scene class name in generated code, defaulting if not found."""
    m = re.search(r"class\\s+(\\w+)\\(Scene\\):", code_text)
    return m.group(1) if m else default


def render_with_manim(out_dir: str, scene_name: str = "ExplainerScene",
                      quality_flag: str = "-ql", output_filename: str = "video.mp4") -> Dict[str, Any]:
    """Render the scene using Manim CLI while the program is running.

    Returns:
        {"success": bool, "data": {"video_path": str}, "error": str}
    """
    try:
        # Run Manim from out_dir so media outputs land there
        cmd = [
            sys.executable, "-m", "manim",
            "scene.py", scene_name,
            quality_flag,              # e.g., -ql, -qm, -qh
            "-o", output_filename,
            "--disable_caching"
        ]
        logger.info("Running: %s", " ".join(cmd))
        subprocess.run(cmd, cwd=out_dir, check=True)
        video_path = os.path.join(out_dir, output_filename)
        return {"success": True, "data": {"video_path": video_path}, "error": ""}
    except subprocess.CalledProcessError as e:
        return {"success": False, "data": None, "error": f"Manim failed: {e}"}
    except FileNotFoundError:
        return {"success": False, "data": None, "error": "Manim not found. Is it installed in this venv?"}
    except Exception as e:
        logger.exception("Render failed")
        return {"success": False, "data": None, "error": str(e)}

