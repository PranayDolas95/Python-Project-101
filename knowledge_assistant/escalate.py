import json
import os
from datetime import datetime

def escalate(query, reason, file_path=None):
    if file_path is None:
        # Get the project root directory (parent of src)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(os.path.dirname(current_dir), "tickets", "escalations.json")
    
    # Ensure the tickets directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    ticket = {
        "query": query,
        "reason": reason,
        "timestamp": datetime.now().isoformat()
    }
    
    # Try to read existing data
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    data = []
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = []
    else:
        data = []
    
    # Append new ticket and write back
    data.append(ticket)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

