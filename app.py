import json
import uuid
from pathlib import Path

from dotenv import load_dotenv
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

from services.exporters import build_comic_pdf
from services.image_generator import generate_panel_images
from services.story_generator import generate_story

BASE_DIR = Path(__file__).resolve().parent
GENERATED = BASE_DIR / "generated"
GENERATED.mkdir(parents=True, exist_ok=True)
DEMO_ASSETS = BASE_DIR / "demo_assets"

app = FastAPI(title="ComicCraft", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
app.mount("/generated", StaticFiles(directory=GENERATED), name="generated")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "ComicCraft",
        "gemini_key_configured": bool(os.getenv("GEMINI_API_KEY", "").strip()),
        "image_model": os.getenv("GEMINI_IMAGE_MODEL", "gemini-nano-banana-2.1"),
    }


@app.post("/api/generate")
async def generate_comic(
    prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form(...),
    art_style: str = Form(...),
    panels: int = Form(4),
):
    data = {
        "prompt": prompt.strip(),
        "character_name": character_name.strip(),
        "setting": setting.strip(),
        "tone": tone.strip(),
        "art_style": art_style.strip(),
        "panels": max(2, min(panels, 8)),
    }

    if not data["prompt"] or not data["character_name"] or not data["setting"]:
        return JSONResponse(
            {"error": "Prompt, character name and setting are required."},
            status_code=400,
        )

    comic_id = uuid.uuid4().hex

    try:
        story = generate_story(data)
    except Exception:
        # Keep the app demoable even when the text API is unavailable.
        story = {
            "title": "The Guardian of the Mystic Forest",
            "panels": [
                {"title": "The Journey Begins", "narration": "A young hero enters a mysterious forest.", "dialogue": "Something is waiting beyond the trees."},
                {"title": "A Strange Light", "narration": "A golden light appears deep inside the forest.", "dialogue": "What is that glow?"},
                {"title": "The Hidden Temple", "narration": "An ancient temple emerges from the mist.", "dialogue": "I finally found it."},
                {"title": "The Guardian", "narration": "The hero faces the magical guardian of the temple.", "dialogue": "I will protect this place."},
            ],
        }

    try:
        panel_images = generate_panel_images(story, data)
        notice = "Comic generated with AI images."
    except Exception as image_exc:
        # Fallback demo artwork prevents a blank result when image API quota is unavailable.
        panel_images = []
        notice = "Image API unavailable; showing bundled reference artwork for demonstration."
        for index in range(len(story["panels"])):
            source = DEMO_ASSETS / f"panel_{(index % 4) + 1}.png"
            if source.exists():
                panel_images.append(source.read_bytes())

        if not panel_images:
            return JSONResponse(
                {"error": f"Comic generation failed: {image_exc}"},
                status_code=500,
            )

    image_urls = []
    for index, image_bytes in enumerate(panel_images[:len(story["panels"])], start=1):
        image_path = GENERATED / f"{comic_id}_panel_{index}.png"
        image_path.write_bytes(image_bytes)
        image_urls.append(f"/generated/{image_path.name}")

    for index, panel in enumerate(story["panels"]):
        panel["image_url"] = image_urls[index]

    return JSONResponse(
        {
            "comic_id": comic_id,
            "title": story["title"],
            "panels": story["panels"],
            "notice": notice,
        }
    )


@app.post("/api/export")
async def export_comic(
    comic_id: str = Form(...),
    title: str = Form(...),
    panels_json: str = Form(...),
):
    try:
        panels = json.loads(panels_json)
    except json.JSONDecodeError:
        return JSONResponse({"error": "Invalid panel data."}, status_code=400)

    if not isinstance(panels, list) or not panels:
        return JSONResponse({"error": "No comic panels supplied."}, status_code=400)

    safe_id = "".join(ch for ch in comic_id if ch.isalnum())
    if not safe_id:
        return JSONResponse({"error": "Invalid comic ID."}, status_code=400)

    pdf_path = GENERATED / f"ComicCraft_{safe_id}.pdf"

    try:
        build_comic_pdf(title, panels, GENERATED, pdf_path)
    except Exception as exc:
        return JSONResponse(
            {"error": f"PDF generation failed: {exc}"},
            status_code=500,
        )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=pdf_path.name,
    )
