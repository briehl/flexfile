from pathlib import Path
from datetime import datetime
import json

INPUT_PATH = Path("data/parsed_workouts.json")
OUTPUT_PATH = Path("data/workout_days.json")

def make_workout_buckets(input_path: Path, output_path: Path):
    with open(input_path, "r") as in_json:
        parsed = json.load(in_json)

    buckets = [{}, {}, {}, {}, {}, {}, {}]
    print(buckets)
    for workout in parsed:
        weekday = datetime.fromisoformat(workout["filename"]).weekday()
        buckets[weekday][workout["filename"]] = workout

    with open(output_path, "w") as out_json:
        json.dump(buckets, out_json, indent=4)

if __name__== "__main__":
    print("running")
    make_workout_buckets(INPUT_PATH, OUTPUT_PATH)
