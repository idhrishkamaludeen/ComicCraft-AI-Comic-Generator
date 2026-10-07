from pathlib import Path
from PIL import Image
from fpdf import FPDF


class ComicPDF(FPDF):
    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", size=8)
        self.cell(0, 8, f"ComicCraft - Page {self.page_no()}", align="C")


def safe_text(value):
    value = str(value or "")
    return value.encode("latin-1", "replace").decode("latin-1")


def build_comic_pdf(title, panels, generated_dir, output_path):
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=False)

    for index, panel in enumerate(panels, start=1):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 10, safe_text(title))
        pdf.ln(12)

        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 8, safe_text(f"Panel {index}: {panel.get('title', '')}"))
        pdf.ln(10)

        image_url = panel.get("image_url", "")
        filename = Path(image_url).name
        image_path = generated_dir / filename

        if not image_path.exists():
            raise FileNotFoundError(f"Generated image not found: {filename}")

        # Convert to RGB JPEG for maximum PDF compatibility.
        temp_path = generated_dir / f"_pdf_{index}_{filename}.jpg"
        with Image.open(image_path) as img:
            img.convert("RGB").save(temp_path, "JPEG", quality=95)

        try:
            pdf.image(str(temp_path), x=10, y=48, w=190, h=107)
        finally:
            try:
                temp_path.unlink()
            except OSError:
                pass

        pdf.set_y(162)
        pdf.set_font("Helvetica", size=10)
        pdf.multi_cell(190, 6, safe_text(panel.get("narration", "")))
        pdf.ln(2)

        pdf.set_font("Helvetica", "I", size=10)
        pdf.multi_cell(190, 6, safe_text(panel.get("dialogue", "")))

    pdf.output(str(output_path))
