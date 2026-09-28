import pytest
from app.matcher import evaluate, parse_skills, skill_in_text
from app.pdf_reader import PDFError, extract_text, guess_candidate_name
from tests.helpers import make_pdf


def test_parse_skills_dedupes_and_cleans():
    assert parse_skills("Python, python ,  Docker;\n\nGit") == ["Python", "Docker", "Git"]


def test_case_insensitive_match():
    assert skill_in_text("DOCKER", "Experienced with docker and Linux")


def test_whole_word_only():
    assert not skill_in_text("Java", "Expert in JavaScript")
    assert skill_in_text("C++", "Languages: C++, Python")


def test_alias_match():
    assert skill_in_text("Kubernetes", "Deployed apps on k8s")


def test_evaluate_partial():
    r = evaluate("Python and Docker experience", "Python, Docker, Kubernetes, Jenkins")
    assert r.percentage == 50.0 and r.missing == ["Kubernetes", "Jenkins"] and not r.shortlisted


def test_evaluate_requires_skills():
    with pytest.raises(ValueError):
        evaluate("text", " , ")


def test_extract_text_and_name():
    pdf = make_pdf(["Jane Doe", "Skills: Python, Docker"])
    text = extract_text(pdf)
    assert "Docker" in text and guess_candidate_name(text, "x.pdf") == "Jane Doe"


def test_name_falls_back_to_filename():
    assert guess_candidate_name("Resume\nemail: a@b.com\n555-1234", "john_cv.pdf") == "john_cv"


def test_invalid_pdf_raises():
    with pytest.raises(PDFError):
        extract_text(b"this is not a pdf")
