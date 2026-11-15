from pathlib import Path
import re
from typing import List, Dict
from collections import defaultdict
import sys


file_path = Path("log_file.log")

def parse_log_line(line: str) -> dict:
    match = re.match(r'(\d{4}(?:-\d{2}){2} \d{2}(?::\d{2}){2}) (\w+) (.*)', line)
    if not match:
        return None
    date_str, level, message = match.groups()
    return {
        "date": date_str,
        "level": level,
        "message": message
    }

def load_logs(file_path: str) -> list:
    try:
        with open(file_path, 'r') as log_file:
            lines = list(filter(lambda x: x is not None,(map(parse_log_line, log_file.readlines()))))
        return lines
    except FileNotFoundError as e:
        print(f"Помилка: файл {file_path} не знайдено.")
        return []

def filter_logs_by_level(logs: list, level: str) -> list:
    return list(filter(lambda x: x['level'] == level, logs))

def count_logs_by_level(logs: list) -> dict:
    cntr = defaultdict(int)
    for log in logs:
        cntr[log['level']] += 1
    return dict(cntr)

def display_log_counts(counts: dict):
    for level, count in counts.items():
        print(f"{level}: {count}")

if __name__ == "__main__":
    filename = sys.argv[1]
    logs = load_logs(filename)
    display_log_counts(count_logs_by_level(logs))
    if len(sys.argv)==3:
        level=sys.argv[2]
        logs=filter_logs_by_level(logs,level)
        print()
        if not logs:
            print(f"Немає логів для рівня '{level}'.")
        else:
            print(f"Деталі логів для рівня '{level}':")
            for x in logs:
                print(f"{x['date']} - {x['message']}")


