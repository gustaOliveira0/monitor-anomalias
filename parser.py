import re
from datetime import datetime

# Expressão regular para reconhecer os logs
LOG_PATTERN = re.compile(r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+(ERROR|INFO|WARNING)\s+(.*)$')

def parse_log_line(line):
    match = LOG_PATTERN.match(line)
    if not match:
        return None
    timestamp_str, level, message = match.groups()
    timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
    return timestamp, level, message
