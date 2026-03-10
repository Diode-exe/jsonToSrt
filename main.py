"""This script reads a JSON file specified by the user
and prints a success message
if the file is loaded correctly."""

import json
import argparse
import sys
import time

timer_start = time.perf_counter()

def seconds_to_srt(sec: float) -> str:
    """Convert seconds to SRT time format (HH:MM:SS,mmm)."""
    total_ms = int(round(sec * 1000))
    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    m = (total_s // 60) % 60
    h = total_s // 3600
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

parser = argparse.ArgumentParser()
parser.add_argument('--file', type=str, help='The JSON file to read from')
args = parser.parse_args()

try:
    with open(args.file, 'r', encoding='utf-8') as fh:
        data = json.load(fh)
    print("JSON file loaded successfully.")
except TypeError as e:
    if not args.file:
        print("No file specified. Please provide a JSON file using the --file argument.")
    else:
        print(f"An error occurred while trying to read the file '{args.file}': {e}.")
    sys.exit(1)
except FileNotFoundError:
    print(f"The file '{args.file}' was not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from '{args.file}': {e}.")
    sys.exit(1)

segments = data.get('segments', [])

srtFile = args.file.rsplit('.', 1)[0] + '.srt'
with open(srtFile, 'w', encoding='utf-8') as f:
    i = 0
    for segment in segments:
        i += 1
        try:
            seg_start = float(segment['start'])
            seg_end = float(segment['end'])
            text = segment['text']
        except (ValueError, TypeError) as e:
            print(f"Error converting segment times to float: {e}")
            continue
        except KeyError as e:
            print(f"Missing expected key in segment: {e}")
            continue
        f.write(f"{i}\n{seconds_to_srt(seg_start)} --> {seconds_to_srt(seg_end)}\n{text}\n\n")

timer_end = time.perf_counter()
print(f"Conversion completed in {timer_end - timer_start:.6f} seconds.")
