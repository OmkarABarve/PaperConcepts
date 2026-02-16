# Manim Paper Agent

Generate Manim animations from research PDFs using a 3-agent pipeline:
1) Analyzer (extracts teachable concepts)
2) Script Generator (directed storyboard JSON)
3) Manim Code Writer (emits executable Python for Manim)

## What you install
- **Python packages (in a virtualenv)**: everything in `manim-paper-agent/requirements.txt` (includes `manim`, `google-generativeai`, etc.)
- **System tools**:
  - **ffmpeg**: required for video encoding (must be on your PATH)
  - **LaTeX** (Windows: **MiKTeX**): required if the generated Manim code uses `MathTex`/LaTeX
- **API key**:
  - `manim-paper-agent/.env` containing `GEMINI_API_KEY=...`

## Install
### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r .\manim-paper-agent\requirements.txt
```

### macOS / Linux (bash/zsh)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r ./manim-paper-agent/requirements.txt
```

### System dependencies checks
- **ffmpeg**: verify with `ffmpeg -version`
- **Manim health check**: run `python -m manim checkhealth`
- **LaTeX**: if you see LaTeX errors, install MiKTeX (Windows) and rerun `python -m manim checkhealth`

## Configure (API key)
Create `manim-paper-agent/.env`:
```env
GEMINI_API_KEY=your_key_here
```

## Run
### Full pipeline (generate + render video)
```bash
python manim-paper-agent/main.py --pdf "path/to/paper.pdf" --out "manim-paper-agent/outputs" --quality low
```

### Generate only (skip rendering)
Use `--no-render` to write outputs without calling Manim:
```bash
python manim-paper-agent/main.py --pdf "path/to/paper.pdf" --out "manim-paper-agent/outputs" --quality low --no-render
```

Artifacts:
- `outputs/analyzer.json` — analyzer JSON
- `outputs/script.json` — directed storyboard
- `outputs/scene.py` — generated Manim code
- `outputs/video.mp4` — rendered video

## How to get a video after using `--no-render`
When you run with `--no-render`, you still get `scene.py`. To render later, run Manim yourself **from the output directory**.

1) **Find the scene class name** inside `scene.py` (look for `class Something(Scene):`).
   - If you don’t want to look, re-run the pipeline without `--no-render` and it will auto-detect the scene class.

2) **Render** (example uses `ExplainerScene` and low quality):
```bash
cd manim-paper-agent/outputs
python -m manim scene.py ExplainerScene -ql -o video.mp4 --disable_caching
```

Quality flags mapping:
- `--quality low` → `-ql`
- `--quality medium` → `-qm`
- `--quality high` → `-qh`

Output:
- Your MP4 will be at `manim-paper-agent/outputs/video.mp4`
- Manim’s usual media tree is under `manim-paper-agent/outputs/media/...`
-Gives:
 File ready at                                                                               
                             'C:\Users\Admin\Desktop\PaperConcepts\manim-paper-agent\outputs\med                         
                             ia\videos\scene\720p30\video.mp4'                                                           
                                                               
* In powershell give command:
Start-Process 'C:\Users\Admin\Desktop\PaperConcepts\manim-paper-agent\outputs\med                         
                             ia\videos\scene\720p30\video.mp4'


## Notes / troubleshooting
- **LaTeX failures**: install MiKTeX and re-run `python -m manim checkhealth`.
- **ffmpeg not found**: install ffmpeg and ensure it’s on PATH, then retry rendering.
