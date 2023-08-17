import os
import subprocess
import sys

# from libs.in_win import inside_windows

current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
exec = sys.executable
# os.popen(f"{exec} v2rayp.py")
subprocess.run([exec, "v2rayp.py"])
