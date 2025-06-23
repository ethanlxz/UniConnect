import os
import subprocess

for root, dirs, files in os.walk("."):
    if "__pycache__" in dirs:
        pycache_path = os.path.join(root, "__pycache__")
        subprocess.run(["git", "rm", "-r", "--cached", pycache_path])
