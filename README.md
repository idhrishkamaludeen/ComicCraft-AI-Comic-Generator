# 🎨 ComicCraft – AI Comic Generator

ComicCraft is an AI-powered web application that transforms user ideas into engaging comic stories with AI-generated comic panels and downloadable PDF output.

The project is built with **Python, FastAPI, Google Gemini AI, HTML, CSS, and JavaScript**.

---

## 🚀 Features

* 🤖 AI-powered comic story generation
* 📝 Custom story prompts
* 👤 Custom character names
* 🌲 Custom settings
* 🎭 Multiple tones and art styles
* 🖼️ AI-generated comic panels
* 🎨 Anime, Manga, Comic and Cartoon styles
* 👀 Real-time comic preview
* 📄 Downloadable PDF comics
* 🔄 Demo artwork fallback when image generation is unavailable
* ⚡ FastAPI backend
* 📱 Responsive web interface
* 🔐 Environment-variable based API key configuration

---

## 🧠 How ComicCraft Works

```text
User Input
    ↓
Comic Prompt
    ↓
Gemini AI Story Generation
    ↓
Panel Descriptions
    ↓
AI Image Generation
    ↓
Comic Panel Images
    ↓
Web Preview
    ↓
PDF Export
```

---

## 🛠️ Technologies Used

* **Python 3.10+**
* **FastAPI**
* **Uvicorn**
* **Google Gemini API**
* **Google GenAI SDK**
* **Jinja2**
* **HTML / CSS / JavaScript**
* **Pillow**
* **FPDF2**
* **python-dotenv**

---

## 📁 Project Structure

```text
comiccraft_project-main/
│
├── services/
│   ├── story_generator.py
│   ├── image_generator.py
│   └── exporters.py
│
├── templates/
│   └── index.html
│
├── static/
│   └── ...
│
├── demo_assets/
│   ├── panel_1.png
│   ├── panel_2.png
│   ├── panel_3.png
│   └── panel_4.png
│
├── generated/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

> The `generated/` folder is used to store generated comic images and PDF files.

---

# ⚙️ Installation

## 1. Clone the Repository

Clone this repository to your computer:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Then enter the project folder:

```bash
cd comiccraft_project-main
```

---

## 2. Create a Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks the activation script, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

Install all required Python packages:

```powershell
pip install -r requirements.txt
```

---

# 🔑 Gemini API Configuration

ComicCraft uses the **Google Gemini API** for AI story and image generation.

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_IMAGE_MODEL=gemini-nano-banana-2.1
```

Replace:

```text
your_gemini_api_key_here
```

with your own Gemini API key.

### ⚠️ Important

**Never upload your `.env` file or API key to GitHub.**

Your `.gitignore` should contain:

```gitignore
.env
.env.*
.venv/
venv/
__pycache__/
*.pyc
```

Each user running ComicCraft should create their own `.env` file with their own API key.

---

# ▶️ Running ComicCraft

After installing the dependencies and configuring the API key, start the FastAPI server:

```powershell
python -m uvicorn app:app --reload
```

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

Open your browser and visit:

```text
http://127.0.0.1:8000
```

You can now use ComicCraft locally.

---

# 🩺 Health Check

ComicCraft includes a health endpoint:

```text
http://127.0.0.1:8000/health
```

It can be used to check whether the application is running.

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can use the Swagger UI to test the available API endpoints.

---

# 🔌 API Endpoints

## Home

```http
GET /
```

Loads the ComicCraft web interface.

---

## Health Check

```http
GET /health
```

Returns the application status and Gemini configuration information.

---

## Generate Comic

```http
POST /api/generate
```

Generates a comic based on the supplied information.

### Parameters

| Parameter        | Description            |
| ---------------- | ---------------------- |
| `prompt`         | Comic story idea       |
| `character_name` | Main character name    |
| `setting`        | Story setting          |
| `tone`           | Story tone             |
| `art_style`      | Visual style           |
| `panels`         | Number of comic panels |

The number of panels is limited to **2–8**.

---

## Export Comic

```http
POST /api/export
```

Creates a downloadable PDF comic.

### Parameters

| Parameter     | Description        |
| ------------- | ------------------ |
| `comic_id`    | Generated comic ID |
| `title`       | Comic title        |
| `panels_json` | Comic panel data   |

---

# 🖼️ Demo Fallback

ComicCraft includes fallback behavior to make the application easier to demonstrate.

If AI story generation is unavailable, the application can use a built-in demo story.

If AI image generation is unavailable, ComicCraft can use the bundled images inside:

```text
demo_assets/
```

Example:

```text
demo_assets/panel_1.png
demo_assets/panel_2.png
demo_assets/panel_3.png
demo_assets/panel_4.png
```

This allows the application to still demonstrate the comic-generation workflow when an image API is unavailable.

---

# 🔐 Security

Do not commit sensitive information to GitHub.

Never upload:

```text
.env
API keys
Passwords
Access tokens
.venv/
venv/
```

Keep API credentials in environment variables.

---

# 🧪 Development

To run the project during development:

```powershell
python -m uvicorn app:app --reload
```

The `--reload` option automatically restarts the server when Python source files are changed.

---

# 📦 Requirements

The project dependencies are listed in:

```text
requirements.txt
```

Install them with:

```powershell
pip install -r requirements.txt
```

---

# 🌟 Future Improvements

Possible future improvements include:

* User accounts
* Comic history
* More AI art styles
* Character consistency improvements
* Multiple-page comic books
* Cloud deployment
* Database integration
* Image editing
* Custom character reference images
* Public comic sharing
* Mobile application

---

# 🤝 Contributing

Contributions are welcome!

To contribute:

1. Fork the repository.
2. Clone your fork.
3. Create a new branch.
4. Make your changes.
5. Test the application.
6. Commit your changes.
7. Push the branch.
8. Create a Pull Request.

Example:

```bash
git checkout -b feature/new-feature
```

---

# 📄 License

This project is available for educational and development purposes.

If you add a specific open-source license to the repository, update this section accordingly.

---

# 👨‍💻 Author

**ComicCraft**

An AI-powered comic generation project built with Python, FastAPI, and Google Gemini.

---

## ⭐ Support

If you find ComicCraft useful, consider giving the repository a ⭐ on GitHub!
