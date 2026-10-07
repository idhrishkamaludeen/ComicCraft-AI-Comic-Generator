"""ComicCraft real image generation using Google's Gemini image model."""

import os
from typing import Any

from google import genai
from google.genai import types


IMAGE_MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-nano-banana-2.1")
IMAGE_SIZE = os.getenv("GEMINI_IMAGE_SIZE", "1K")
ASPECT_RATIO = os.getenv("GEMINI_IMAGE_ASPECT_RATIO", "16:9")


def _get_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Create a .env file in the ComicCraft folder "
            "and add: GEMINI_API_KEY=your_key_here"
        )
    return genai.Client(api_key=api_key)


def _extract_image_bytes(response: Any) -> bytes:
    """Extract the first actual image returned by Gemini."""
    candidates = getattr(response, "candidates", None) or []

    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []

        for part in parts:
            inline_data = getattr(part, "inline_data", None)
            if inline_data is not None:
                data = getattr(inline_data, "data", None)
                if data:
                    return data

            # SDKs may expose the same payload as inlineData.
            inline_data = getattr(part, "inlineData", None)
            if inline_data is not None:
                data = getattr(inline_data, "data", None)
                if data:
                    return data

    raise RuntimeError(
        "Gemini returned no image. Make sure your API key has access to "
        f"the image model '{IMAGE_MODEL}'."
    )


def _build_visual_prompt(data: dict, panel: dict, index: int) -> str:
    style = data["art_style"].strip().lower()

    if style == "anime":
        style_instruction = (
            "high-quality original anime illustration, Japanese animation-inspired "
            "character design, expressive eyes, clean line art, cel shading, "
            "dynamic cinematic composition"
        )
    elif style in {"comic book", "comic"}:
        style_instruction = (
            "professional comic-book illustration, bold ink linework, dynamic panel "
            "composition, dramatic lighting, rich colors, detailed backgrounds"
        )
    elif style == "manga":
        style_instruction = (
            "original manga-style illustration, expressive character acting, clean "
            "ink lines, screentone-inspired shading, cinematic framing"
        )
    elif style == "cartoon":
        style_instruction = (
            "polished animated cartoon illustration, expressive shapes, clean outlines, "
            "appealing character design, cinematic background"
        )
    else:
        style_instruction = f"professional {style} illustration with cinematic composition"

    return f"""
Generate ONE actual image for a comic panel.

IMPORTANT OUTPUT RULE:
Return a finished VISUAL ILLUSTRATION. Do NOT return a written description,
plain text, a prompt, a text-only poster, or a page containing instructions.

ORIGINAL USER STORY IDEA:
{data["prompt"]}

MAIN CHARACTER:
{data["character_name"]}

SETTING:
{data["setting"]}

TONE:
{data["tone"]}

ART STYLE:
{style_instruction}

PANEL {index} OF {data["panels"]}:
{panel.get("image_prompt", "")}

STORY NARRATION FOR THIS PANEL:
{panel.get("narration", "")}

DIALOGUE CONTEXT:
{panel.get("dialogue", "")}

VISUAL GOAL:
Show the actual characters, environment, action, facial expressions, lighting,
depth, and mood described by the story. Make the scene look like a finished
professional comic/anime panel.

CONSISTENCY:
Keep the main character's appearance consistent across panels: same face,
hair, clothing, colors, age, and body proportions.

DO NOT INCLUDE:
speech bubbles, captions, subtitles, paragraphs, prompt text, UI elements,
logos, watermarks added by the prompt, or a blank/text-only image.

Fill the complete frame with artwork.
""".strip()


def generate_panel_images(story: dict, data: dict) -> list[bytes]:
    """Generate one real PNG image for every panel."""
    client = _get_client()
    images: list[bytes] = []

    for index, panel in enumerate(story["panels"], start=1):
        prompt = _build_visual_prompt(data, panel, index)

        try:
            response = client.models.generate_content(
                model=IMAGE_MODEL,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=["IMAGE"],
                    response_format={
                        "image": {
                            "aspect_ratio": ASPECT_RATIO,
                            "image_size": IMAGE_SIZE,
                        }
                    },
                ),
            )
            images.append(_extract_image_bytes(response))
        except Exception as exc:
            raise RuntimeError(
                f"Image generation failed for panel {index}: {exc}"
            ) from exc

    return images
