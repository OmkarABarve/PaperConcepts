import json
from utils.validation import validate_script


def test_generator_schema_example():
    # Minimal valid storyboard example to validate schema function
    storyboard = {
        "video_title": "Title",
        "concept_id": "c1",
        "duration_sec": 60,
        "scenes": [
            {
                "id": "scene_1",
                "steps": [
                    {"action": "add_text", "id": "t1", "content": "Hello", "at": "CENTER", "color": "WHITE", "scale": 1.0},
                    {"action": "wait", "seconds": 0.5}
                ]
            }
        ]
    }
    validate_script(storyboard)

