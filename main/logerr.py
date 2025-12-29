import os
from datetime import datetime

def logerr(e):
    # Ensure the 'out' directory exists
    os.makedirs('out', exist_ok=True)
    
    # Open the file in append mode ('a') so previous logs aren't overwritten
    with open('out/errors.txt', 'a') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {e}\n")

# TO DO add email notification