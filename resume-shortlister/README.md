# Resume Shortlister

A small FastAPI web app that reads an uploaded resume PDF and checks it against a job's required skills
using simple keyword matching (no AI, no ML, no external APIs, no database).

**For each resume it shows:** matching skills, missing skills, match percentage, and a
shortlisted / not shortlisted decision (default threshold: 60%, adjustable in the form).

## How it works
1. The user uploads a **resume PDF**, enters the **required skills** and a **threshold**.
2. `pypdf` extracts the text from the PDF (`app/pdf_reader.py`).
3. The candidate name is the first of the top 5 lines that looks like a 2-4 word name; otherwise the **file name** is used.
4. Each required skill is searched in the resume text (case-insensitive, whole-word, so `Java` does not match `JavaScript`).
   A few aliases are treated as equal (e.g. `k8s` = `kubernetes`, see `ALIASES` in `app/matcher.py`).
5. `match % = matched skills / required skills × 100`. Shortlisted if `match % >= threshold`.

**Limits:** scanned/image-only PDFs have no text (no OCR), password-protected PDFs are rejected, and uploads are capped at 5 MB.

## Project structure
```
resume-shortlister/
├── app/
│   ├── main.py          # FastAPI routes (/, /evaluate, /health)
│   ├── pdf_reader.py    # PDF text extraction + name guess (pypdf)
│   ├── matcher.py       # Keyword skill-matching logic
│   ├── templates/       # index.html (Jinja2)
│   └── static/          # style.css
├── tests/               # pytest tests
├── Dockerfile
├── Jenkinsfile          # CI/CD pipeline
├── requirements.txt     # runtime deps
├── requirements-dev.txt # runtime + test deps
└── README.md
```

## Run locally
```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```
Open http://localhost:8000 · Health check: http://localhost:8000/health · API docs: http://localhost:8000/docs

## Run tests
```bash
pytest -q
```

## Run with Docker
```bash
docker build -t resume-shortlister .
docker run -d --name resume-shortlister -p 8000:8000 resume-shortlister
curl http://localhost:8000/health
```

## Jenkins
The `Jenkinsfile` runs: **Checkout → Install & Test → Build Docker image → Deploy container → Smoke test (`/health`)**.
1. Use a Jenkins agent with Python 3, Docker and curl installed (the `jenkins` user must be in the `docker` group).
2. Create a *Pipeline* (or Multibranch Pipeline) job pointing at your Git repo.
3. Run the build; the app will be available on port 8000 of the Jenkins agent.

## Ideas to extend
Push the image to Docker Hub/ECR, deploy to a remote server via SSH, add Prometheus metrics,
or store evaluations in SQLite.
