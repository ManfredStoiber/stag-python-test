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
print("Run command: delvewheel repair (without arguments)", flush=True)
subprocess.run(["delvewheel",  "repair"], check=True)

print("Run command: ", flush=True)
print(" ".join(["delvewheel",  "repair", "--add-path", f"{path}", "-w", f"{sys.argv[1]}", f"{sys.argv[2]}"]))
print(f"Check if {path} exits: {os.path.exists(path)}")
print(f"Check if {sys.argv[1]} exits: {os.path.exists(sys.argv[1])}", flush=True)
print(f"Check if {sys.argv[2]} exits: {os.path.exists(sys.argv[2])}", flush=True)
subprocess.run(["delvewheel",  "repair", "--add-path", f"{path}", "-w", f"{sys.argv[1]}", f"{sys.argv[2]}"])