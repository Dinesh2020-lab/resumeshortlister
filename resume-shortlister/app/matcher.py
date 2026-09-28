"""Rule-based skill matching. No ML, no external APIs."""
import re
from dataclasses import dataclass

# Alias pairs so "k8s" and "kubernetes" count as the same skill. Extend as needed.
ALIASES = {
    "k8s": "kubernetes",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "tf": "terraform",
}


@dataclass
class MatchResult:
    matching: list[str]
    missing: list[str]
    percentage: float
    shortlisted: bool
    threshold: int


def parse_skills(raw: str) -> list[str]:
    """Split on commas/semicolons/new lines; remove blanks and duplicates (case-insensitive)."""
    seen, skills = set(), []
    for part in re.split(r"[,\n;]+", raw):
        skill = part.strip()
        if skill and skill.lower() not in seen:
            seen.add(skill.lower())
            skills.append(skill)
    return skills


def _variants(skill: str) -> set[str]:
    """The skill plus any alias/canonical form of it, e.g. k8s <-> kubernetes."""
    s = skill.lower()
    out = {s}
    for alias, canonical in ALIASES.items():
        if s == alias:
            out.add(canonical)
        elif s == canonical:
            out.add(alias)
    return out


def skill_in_text(skill: str, text: str) -> bool:
    """Case-insensitive whole-word search, so 'java' does not match 'javascript'."""
    text = re.sub(r"\s+", " ", text.lower())
    for v in _variants(skill):
        pattern = r"(?<![a-z0-9+#])" + re.escape(v) + r"(?![a-z0-9+#])"
        if re.search(pattern, text):
            return True
    return False


def evaluate(resume_text: str, required_skills: str, threshold: int = 60) -> MatchResult:
    required = parse_skills(required_skills)
    if not required:
        raise ValueError("Please enter at least one job-required skill.")

    matching = [s for s in required if skill_in_text(s, resume_text)]
    missing = [s for s in required if s not in matching]
    percentage = round(len(matching) / len(required) * 100, 1)
    return MatchResult(matching, missing, percentage, percentage >= threshold, threshold)
