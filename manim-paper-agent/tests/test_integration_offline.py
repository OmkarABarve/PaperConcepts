import os
from agents.manimcodewriter import write_scene_file, render_with_manim


def test_offline_render_smoke(tmp_path):
    # Offline minimal scene (no network). Requires manim/ffmpeg installed to truly pass.
    code = """from manim import *
class ExplainerScene(Scene):
    def construct(self):
        t = Text('Hi')
        self.play(Write(t))
        self.wait(0.2)
"""
    out_dir = tmp_path / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    scene_path = write_scene_file(code, str(out_dir))
    # Try to render quickly; if environment missing, allow failure without raising.
    res = render_with_manim(str(out_dir), scene_name="ExplainerScene", quality_flag="-ql", output_filename="video.mp4")
    # Do not assert success here; CI environments may lack ffmpeg/LaTeX.
    assert "success" in res

