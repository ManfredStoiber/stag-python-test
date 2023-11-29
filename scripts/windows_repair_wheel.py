import os
import re
import subprocess
import sys

pattern = re.compile(".*temp.*Release.*opencv.*bin.*Release")

# find opencv dll directory
for d in os.walk('.'):
    if pattern.fullmatch(d[0]):
        path = d[0]
        break

# run delvewheel
print("Run command: ", flush=True)
print(" ".join(["delvewheel",  "repair", "--add-path", f"{path}", "-w", f"{sys.argv[1]}", f"{sys.argv[2]}"]))
subprocess.run(["delvewheel",  "repair", "--add-path", f"{path}", "-w", f"{sys.argv[1]}", f"{sys.argv[2]}"])