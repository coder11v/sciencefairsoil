import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


from sensors import *

if __name__ == "__main__":
    raw = get_moisture_raw("a1")
    per = get_moisture("a1")
    print(f"\nRaw: {raw}\nPercentage: {per}\n")