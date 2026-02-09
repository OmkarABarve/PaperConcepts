import argparse
import json
import os
import sys
from typing import Any, Dict

from rich import print

from agents.analyzer import analyze_paper
from agents.generator import generate_directed_script
from agents.manimcodewriter import (
    generate_manim_code,
    write_scene_file,
    render_with_manim,
    detect_scene_class,
)
from utils.validation import validate_script
from shutil import which


def run(pdf_path: str, out_dir: str, scene_class: str, quality: str, render: bool) -> int:
    os.makedirs(out_dir, exist_ok=True)

    # Basic environment checks
    if which("ffmpeg") is None:
        print("[yellow]Warning: ffmpeg not found. Manim may fail to render video.[/yellow]")

    print("[bold cyan]1) Analyzing PDF...[/bold cyan]")
    an = analyze_paper(pdf_path)
    if not an["success"]:
        print(f"[red]Analyze failed:[/red] {an['error']}")
        return 1

    # Prefer raw JSON text to preserve model intent; fall back to parsed if needed
    analyzer_raw = an["data"]["raw"] if an["data"] else ""
    if not analyzer_raw:
        print("[red]No analyzer output[/red]")
        return 1

    # Save analyzer output
    analyzer_path = os.path.join(out_dir, "analyzer.json")
    with open(analyzer_path, "w", encoding="utf-8") as f:
        f.write(analyzer_raw)
    print(f"[green]Saved:[/green] {analyzer_path}")

    print("[bold cyan]2) Generating directed script...[/bold cyan]")
    sg = generate_directed_script(analyzer_raw)
    if not sg["success"]:
        print(f"[red]Script generation failed:[/red] {sg['error']}")
        return 1

    script_raw = sg["data"]["raw"] if sg["data"] else ""
    if not script_raw:
        print("[red]No script output[/red]")
        return 1

    # Validate script JSON
    try:
        script_parsed = json.loads(script_raw)
        validate_script(script_parsed)
    except Exception as e:
        print(f"[red]Directed script validation failed:[/red] {e}")
        return 1

    # Save directed script
    script_path = os.path.join(out_dir, "script.json")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_raw)
    print(f"[green]Saved:[/green] {script_path}")

    print("[bold cyan]3) Writing Manim code...[/bold cyan]")
    cw = generate_manim_code(script_raw)
    if not cw["success"]:
        print(f"[red]Code writer failed:[/red] {cw['error']}")
        return 1

    code_text = cw["data"]["code"]
    scene_file = write_scene_file(code_text, out_dir)
    print(f"[green]Saved:[/green] {scene_file}")

    if not render:
        print("[yellow]Render skipped (--no-render used).[/yellow]")
        return 0

    print("[bold cyan]4) Rendering with Manim...[/bold cyan]")
    quality_flag = {"low": "-ql", "medium": "-qm", "high": "-qh"}.get(quality, "-ql")
    # Detect scene class if possible
    detected_scene = detect_scene_class(code_text, default=scene_class)
    rend = render_with_manim(out_dir, scene_name=detected_scene, quality_flag=quality_flag, output_filename="video.mp4")
    if not rend["success"]:
        print(f"[red]Render failed:[/red] {rend['error']}")
        return 1

    print(f"[bold green]Done.[/bold green] Video: {rend['data']['video_path']}")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Manim Paper Agent pipeline")
    parser.add_argument("--pdf", required=True, help="Path to input PDF")
    parser.add_argument("--out", default="manim-paper-agent/outputs", help="Output directory")
    parser.add_argument("--scene-class", default="ExplainerScene", help="Scene class name to render")
    parser.add_argument("--quality", choices=["low", "medium", "high"], default="low", help="Render quality")
    parser.add_argument("--no-render", action="store_true", help="Skip rendering (only write files)")
    args = parser.parse_args()

    try:
        code = run(
            pdf_path=args.pdf,
            out_dir=args.out,
            scene_class=args.scene_class,
            quality=args.quality,
            render=not args.no_render,
        )
        sys.exit(code)
    except KeyboardInterrupt:
        print("[yellow]Interrupted by user[/yellow]")
        sys.exit(130)


if __name__ == "__main__":
    main()