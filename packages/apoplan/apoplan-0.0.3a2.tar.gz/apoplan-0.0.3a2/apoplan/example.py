import os
import subprocess  # nosec
import sys

sys.exit(subprocess.call([ # nosec
    os.path.join(os.path.dirname(__file__), 'bauplan-cli'),
    *sys.argv[1:]
]))
