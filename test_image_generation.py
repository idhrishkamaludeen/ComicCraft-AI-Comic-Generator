"""Quick Gemini image-generation test for ComicCraft.

Run from the ComicCraft folder:
    python test_image_generation.py
"""
from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path
from services.image_generator import generate_panel_images

data = {
    "prompt": "A brave young explorer enters an enchanted forest and discovers a glowing golden lion.",
    "character_name": "Alan",
    "setting": "Enchanted Forest",
    "tone": "adventurous",
    "art_style": "anime",
    "panels": 1,
}
story = {
    "title": "Test",
    "panels": [{
        "title": "The Discovery",
        "narration": "Alan enters the enchanted forest and sees a glowing golden lion.",
        "dialogue": "Alan: What is that?",
        "image_prompt": "Alan standing in a mysterious forest, looking at a majestic glowing golden lion between ancient trees."
    }]
}
images = generate_panel_images(story, data)
path = Path("generated") / "TEST_anime_panel.png"
path.parent.mkdir(exist_ok=True)
path.write_bytes(images[0])
print(f"SUCCESS: real image generated -> {path.resolve()}")
