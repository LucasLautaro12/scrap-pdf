import os
import subprocess

def check_and_update():
    print("Verificando actualizaciones...")
    repo_path = os.path.dirname(os.path.dirname(__file__))
    subprocess.run(["git", "-C", repo_path, "pull"])
