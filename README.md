# ComicCraft - Real AI Image Edition

## What was fixed
- Removed the old text/placeholder PNGs from `generated/`.
- Image generation now uses Gemini's native image-generation endpoint through `client.models.generate_content(...)`.
- The API is explicitly requested to return `IMAGE` output.
- Anime/comic/manga/cartoon styles are turned into strong visual instructions.
- The original user prompt is passed into every visual panel prompt.
- PDF export embeds the generated PNG image, not the prompt text.
- Added `test_image_generation.py` to verify image generation before running the web app.

Google's current Gemini documentation shows `gemini-nano-banana-2.1` for text-to-image generation and supports image-only output. See the official docs linked below.

## Run on Windows / VS Code

Open THIS folder in VS Code:

`comiccraft_project-main\ComicCraft`

PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and set:

```text
GEMINI_API_KEY=YOUR_REAL_GEMINI_API_KEY
GEMINI_MODEL=gemini-2.5-flash
GEMINI_IMAGE_MODEL=gemini-nano-banana-2.1
GEMINI_IMAGE_SIZE=1K
GEMINI_IMAGE_ASPECT_RATIO=16:9
```

Then test the image API first:

```powershell
python test_image_generation.py
```

You should see:

`SUCCESS: real image generated -> ...\generated\TEST_anime_panel.png`

Open that PNG. It must be an actual anime image.

Then start ComicCraft:

```powershell
python -m uvicorn app:app --reload
```

Open:

`http://127.0.0.1:8000`

## Important
A Gemini API key is required for real AI image generation. The ZIP does not contain a secret key.

If the test command fails, copy the complete error shown in the terminal; that error will normally indicate API-key validity, model access, billing/quota, or package/version issues.

## Official Gemini image generation docs
https://ai.google.dev/gemini-api/docs/image-generation


### Demo fallback
If the image-generation API is unavailable or its quota is temporarily exhausted, ComicCraft automatically uses the bundled `demo_assets/` reference artwork so the UI and PDF export can still be demonstrated.
