# Manim Paper Agent

Generate Manim animations from research PDFs using a 3-agent pipeline:
1) Analyzer (extracts teachable concepts)
2) Script Generator (directed storyboard JSON)
3) Manim Code Writer (emits executable Python for Manim)

## Requirements
- Python 3.10+
- Dependencies (install in venv):
  - `pip install -r manim-paper-agent/requirements.txt`
- System tools:
  - ffmpeg (on PATH)
  - TeX distribution (MiKTeX on Windows) for MathTex; run `manim check`
- Secrets:
  - `manim-paper-agent/.env` with `GEMINI_API_KEY=your_key`

## Quickstart
```bash
python manim-paper-agent/main.py --pdf "path/to/paper.pdf" --out "manim-paper-agent/outputs" --quality low
```

Artifacts:
- `outputs/analyzer.json` — analyzer JSON
- `outputs/script.json` — directed storyboard
- `outputs/scene.py` — generated Manim code
- `outputs/video.mp4` — rendered video

## Notes
- If equations fail (LaTeX), ensure MiKTeX is installed and `manim check` passes.
- Use `--no-render` to skip rendering and inspect generated files.
