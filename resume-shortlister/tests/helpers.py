from io import BytesIO
from reportlab.pdfgen import canvas


def make_pdf(lines: list[str]) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf)
    y = 800
    for line in lines:
        c.drawString(72, y, line)
        y -= 20
    c.save()
    return buf.getvalue()
