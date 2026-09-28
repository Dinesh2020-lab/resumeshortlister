"""PDF text extraction and candidate-name guess. Uses pypdf only (pure Python, offline)."""
import re
from io import BytesIO
from pathlib import Path
from pypdf import PdfReader


class PDFError(ValueError):
    """Raised when a PDF cannot be read or has no text."""


def extract_text(file_bytes: bytes) -> str:
    try:
        reader = PdfReader(BytesIO(file_bytes))
        if reader.is_encrypted:
            raise PDFError("This PDF is password-protected. Please upload an unlocked copy.")
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
    except PDFError:
        raise
    except Exception as exc:
        raise PDFError("Could not read this file. Please upload a valid PDF.") from exc
    if not text.strip():
        raise PDFError("No text found in this PDF. It may be a scanned image (OCR is not supported).")
    return text


_NAME_RE = re.compile(r"^[A-Za-z][A-Za-z.'-]*(?: [A-Za-z][A-Za-z.'-]*){1,3}$")
_SKIP_WORDS = {"resume", "curriculum", "vitae", "cv", "profile", "summary", "objective"}


def guess_candidate_name(text: str, filename: str) -> str:
    """Rule: the first of the top 5 non-empty lines that looks like a 2-4 word name.
    Falls back to the file name (without .pdf) if none is found."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()][:5]
    for line in lines:
        words = {w.lower() for w in line.split()}
        if _NAME_RE.match(line) and not words & _SKIP_WORDS:
            return line
    return Path(filename).stem or "Unknown candidate"
