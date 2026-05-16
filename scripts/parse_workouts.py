from pathlib import Path
import json
import re

from parse_bodyweight_email import Exercise, WorkoutType


INPUT_PATH = Path("data/cleaned_emails.json")
OUTPUT_PATH = Path("data/parsed_workouts.json")

# numbered list item: "1. <name> / <reps>" possibly spanning multiple lines
ITEM_RE = re.compile(r"^\s*\d+\.\s+(.+?)(?=^\s*\d+\.|\Z)", re.MULTILINE | re.DOTALL)
NAME_REPS_SPLIT_RE = re.compile(r"\s+/\s+")
WS_RE = re.compile(r"\s+")


def detect_workout_type(text: str) -> WorkoutType | None:
    # workout type is announced near the top; check head only
    head = text[:300]
    # order matters: cardio's first line contains "circuit"; ladder lines
    # often mention "circuit" too
    if "mobility" in head:
        return WorkoutType.MOBILITY
    if "cardio" in head:
        return WorkoutType.CARDIO
    if "pyramid" in head:
        return WorkoutType.PYRAMID
    if "ladder" in head and not "circuit" in head:
        return WorkoutType.LADDER
    if "ladder" in head and "circuit" in head:
        return WorkoutType.LADDER_CIRCUIT
    if "circuit" in head:
        return WorkoutType.CIRCUIT
    if "timed circuit" in head:
        return WorkoutType.TIMED_CIRCUIT
    return None


def parse_exercises(text: str) -> list[Exercise]:
    # NBSP confuses the splitters; normalize to regular space
    normalized = text.replace("\xa0", " ")
    exercises: list[Exercise] = []
    for match in ITEM_RE.finditer(normalized):
        block = match.group(1).strip()
        parts = NAME_REPS_SPLIT_RE.split(block, maxsplit=1)
        if len(parts) != 2:
            continue
        name = WS_RE.sub(" ", parts[0]).strip()
        reps = WS_RE.sub(" ", parts[1]).strip()
        exercises.append(Exercise(name=name, reps=reps))
    return exercises


def main() -> None:
    data = json.loads(INPUT_PATH.read_text(encoding="utf-8"))
    results = []
    for item in data:
        email = item.get("email")
        if not email:
            results.append({
                "filename": item["filename"],
                "workout_type": None,
                "exercises": [],
            })
            continue
        workout_type = detect_workout_type(email)
        exercises = parse_exercises(email)
        results.append({
            "filename": item["filename"],
            "workout_type": workout_type.name if workout_type else None,
            "exercises": [e.model_dump() for e in exercises],
        })
    OUTPUT_PATH.write_text(json.dumps(results, indent=4), encoding="utf-8")
    print(f"wrote {len(results)} parsed workouts to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
