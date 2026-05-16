from email.parser import Parser
from email.policy import default as DefaultPolicy
from pathlib import Path
import json
import sys
from pydantic import BaseModel
from enum import IntEnum
import re


class Exercise(BaseModel):
    name: str
    reps: str
    video: str | None = None

class WorkoutType(IntEnum):
    CIRCUIT = 1
    LADDER = 2
    CARDIO = 3
    MOBILITY = 4
    PYRAMID = 5
    TIMED_CIRCUIT = 6
    LADDER_CIRCUIT = 7

class Workout(BaseModel):
    workout_type: WorkoutType

def parse_email(email_path: Path) -> str:
    if not email_path.exists():
        raise FileNotFoundError(f"email file {email_path} not found")
    with open(email_path) as inmail:
        message = Parser(policy=DefaultPolicy).parse(inmail)
        body = message.get_body(preferencelist=("plain",)).get_content()
        return clean_email(body)

def clean_email(body: str) -> str | None:
    body = body.lower()
    # 1. strip links: <http://...>, <mailto:...>, and bare http(s) URLs
    body = re.sub(r"<(?:https?|mailto):[^>]*>", "", body)
    body = re.sub(r"https?://\S+", "", body)
    # 2. get sentence with "Today's 15 minute workout is..."
    type_sentence_re = re.compile(r"today\'s\s(.+)that\'s\s+all\s+for\s+today", re.DOTALL)
    match = type_sentence_re.search(body)
    cleaned = match.group(1) if match else None
    if cleaned is None:
        cardio_re = re.compile(r"(bodyweight \'cardio\'.+)that\'s\s+all\s+for\s+today", re.DOTALL)
        match = cardio_re.search(body)
        cleaned = match.group(1) if match else None
    return cleaned

def parse_all_emails():
    # This will run clean_email over all files in data/emails
    # and save the results to a file as a list of JSON objects.
    # Each object will have values:
    # filename: the name of the file (not the full path)
    # email: the cleaned email from clean_email for that file
    # The file created will be data/cleaned_emails.json
    emails_dir = Path("data/emails")
    output_path = Path("data/cleaned_emails.json")
    results = []
    stripped_name_re = re.compile(r"(\d{4}-\d{2}-\d{2})")
    for email_path in sorted(emails_dir.iterdir()):
        if not email_path.is_file():
            continue
        match = stripped_name_re.search(email_path.name, re.DOTALL)
        stripped_name = match.group(1)
        results.append({
            "filename": stripped_name,
            "email": parse_email(email_path)
        })
    with open(output_path, "w") as outfile:
        json.dump(results, outfile, indent=4)
    print(f"wrote {len(results)} cleaned emails to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        parse_all_emails()
    else:
        print(parse_email(Path(sys.argv[1])))