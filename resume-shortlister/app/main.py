from pathlib import Path
from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.matcher import evaluate
from app.pdf_reader import PDFError, extract_text, guess_candidate_name

BASE_DIR = Path(__file__).resolve().parent
MAX_UPLOAD_BYTES = 5 * 1024 * 1024  # 5 MB

app = FastAPI(title="Resume Shortlister", version="2.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(request, "index.html", {"form": {"threshold": 60}})


@app.post("/evaluate", response_class=HTMLResponse)
def evaluate_resume(
    request: Request,
    resume: UploadFile = File(...),
    required_skills: str = Form(...),
    threshold: int = Form(60),
):
    form = {"required_skills": required_skills, "threshold": max(0, min(100, threshold))}
    ctx = {"form": form}
    try:
        filename = resume.filename or "resume.pdf"
        if not filename.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported.")
        data = resume.file.read(MAX_UPLOAD_BYTES + 1)
        if not data:
            raise ValueError("The uploaded file is empty.")
        if len(data) > MAX_UPLOAD_BYTES:
            raise ValueError("File is too large (maximum 5 MB).")

        text = extract_text(data)                       # 1. PDF -> text
        ctx["candidate"] = guess_candidate_name(text, filename)  # 2. name or filename
        ctx["result"] = evaluate(text, required_skills, form["threshold"])  # 3. keyword match
    except ValueError as exc:  # PDFError is a ValueError too
        ctx["error"] = str(exc)
        return templates.TemplateResponse(request, "index.html", ctx, status_code=400)
    return templates.TemplateResponse(request, "index.html", ctx)
