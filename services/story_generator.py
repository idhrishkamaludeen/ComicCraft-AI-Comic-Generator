import importlib
import json
import os
import re
from textwrap import dedent


def _load_genai():
    """Load the optional Google Gemini SDK without causing editor import errors."""
    try:
        return importlib.import_module("google.genai")
    except ImportError:
        return None


MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def fallback_story(data):
    name = data["character_name"]
    setting = data["setting"]
    tone = data["tone"]
    style = data["art_style"]
    prompt = data["prompt"]
    count = data["panels"]

    templates = [
        {
            "title": "The First Step",
            "narration": f"{name} enters {setting}, ready to face the mystery described in the adventure: {prompt}.",
            "dialogue": f"{name}: Something tells me this journey is only beginning!",
        },
        {
            "title": "A Strange Discovery",
            "narration": f"A surprising clue appears, changing what {name} thought was possible.",
            "dialogue": f"{name}: I have never seen anything like this before!",
        },
        {
            "title": "The Challenge",
            "narration": f"The path becomes difficult, but {name} refuses to give up.",
            "dialogue": f"{name}: Whatever happens, I will keep moving forward!",
        },
        {
            "title": "A New Beginning",
            "narration": f"The mystery begins to make sense, leaving {name} with a new purpose.",
            "dialogue": f"{name}: This is not the end. It is the beginning of a new adventure!",
        },
        {
            "title": "The Hidden Secret",
            "narration": f"{name} discovers one final clue hidden within {setting}.",
            "dialogue": f"{name}: Now I understand what the clues were trying to tell me.",
        },
        {
            "title": "The Unexpected Friend",
            "narration": f"An unexpected companion appears and helps {name} solve the next part of the mystery.",
            "dialogue": f"{name}: Maybe we are stronger when we work together.",
        },
        {
            "title": "The Final Test",
            "narration": f"{name} faces the final test and remembers everything learned along the journey.",
            "dialogue": f"{name}: Courage is choosing to continue even when I am afraid.",
        },
        {
            "title": "Adventure Continues",
            "narration": f"The adventure ends for today, but a distant mystery promises another story.",
            "dialogue": f"{name}: I have a feeling there is another adventure waiting for us!",
        },
    ]

    panels = []
    for i in range(count):
        item = templates[i % len(templates)].copy()
        item["image_prompt"] = (
            f"{style} comic illustration, {tone} mood, consistent character named {name}, "
            f"setting: {setting}, panel {i + 1}, cinematic composition, expressive face, "
            f"clear subject, no text, no speech bubbles, story context: {prompt}"
        )
        panels.append(item)

    return {"title": f"{name}'s Adventure", "panels": panels}


def _extract_json(text):
    text = (text or "").strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model did not return JSON.")

    return json.loads(text[start : end + 1])


def generate_story(data):
    api_key = os.getenv("GEMINI_API_KEY")
    genai = _load_genai()

    # The local fallback keeps the application usable without an API key or SDK.
    if not api_key or genai is None:
        return fallback_story(data)

    try:
        client = genai.Client(api_key=api_key)

        prompt = dedent(
            f"""
            Create a short original comic story as structured JSON.

            User prompt: {data["prompt"]}
            Main character: {data["character_name"]}
            Setting: {data["setting"]}
            Tone: {data["tone"]}
            Art style: {data["art_style"]}
            Number of panels: {data["panels"]}

            Requirements:
            - Return ONLY valid JSON.
            - Use exactly {data["panels"]} panels.
            - Maintain character and setting consistency.
            - Each panel needs: title, narration, dialogue, image_prompt.
            - image_prompt must describe the visual scene but must NOT request written text,
              captions, speech bubbles, logos, or watermarks inside the image.
            - Keep dialogue short.
            - Make the story family-friendly and original.

            JSON format:
            {{
              "title": "Comic title",
              "panels": [
                {{
                  "title": "Panel title",
                  "narration": "Narration",
                  "dialogue": "Character dialogue",
                  "image_prompt": "Detailed visual prompt"
                }}
              ]
            }}
            """
        )

        response = client.models.generate_content(model=MODEL, contents=prompt)
        result = _extract_json(getattr(response, "text", ""))

        panels = result.get("panels", [])
        if not isinstance(panels, list) or len(panels) != data["panels"]:
            return fallback_story(data)

        return result
    except Exception:
        # Never make a temporary Gemini/API problem break the entire web app.
        return fallback_story(data)
