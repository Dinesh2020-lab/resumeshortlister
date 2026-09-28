from fastapi.testclient import TestClient
from app.main import app
from tests.helpers import make_pdf

client = TestClient(app)


def _post(pdf_bytes, filename="resume.pdf", skills="Python, Docker", threshold=60):
    return client.post(
        "/evaluate",
        data={"required_skills": skills, "threshold": threshold},
        files={"resume": (filename, pdf_bytes, "application/pdf")},
    )


def test_health():
    assert client.get("/health").json() == {"status": "ok"}


def test_home_page_has_upload_form():
    r = client.get("/")
    assert r.status_code == 200 and 'type="file"' in r.text


def test_shortlisted():
    r = _post(make_pdf(["Jane Doe", "Python, Docker, Git"]))
    assert r.status_code == 200
    assert "Jane Doe" in r.text and "Shortlisted" in r.text and "100.0%" in r.text


def test_not_shortlisted_shows_missing():
    r = _post(make_pdf(["Jane Doe", "Python"]), skills="Python, Docker, Jenkins, Kubernetes")
    assert "Not shortlisted" in r.text and "Jenkins" in r.text


def test_filename_used_when_no_name():
    r = _post(make_pdf(["email: a@b.com", "Skills: Python, Docker"]), filename="john_cv.pdf")
    assert "john_cv" in r.text


def test_rejects_non_pdf():
    r = _post(b"hello", filename="notes.txt")
    assert r.status_code == 400 and "Only PDF" in r.text


def test_rejects_corrupt_pdf():
    assert _post(b"not really a pdf").status_code == 400
