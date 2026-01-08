import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from sensors import *

if __name__ == "__main__":
    # Reading for a1
    raw_a1 = get_moisture_raw("a1")
    per_a1 = get_moisture("a1")
    print(f"Dumb:\n(a1) \nRaw: {raw_a1}\nPercentage: {per_a1}\n")

    # Reading for a0
    raw_a0 = get_moisture_raw("a0")
    per_a0 = get_moisture("a0")
    print(f"Smart:\n(a0) \nRaw: {raw_a0}\nPercentage: {per_a0}\n")