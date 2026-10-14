import shutil
import subprocess


class Btop:

    def is_available(self):
        return shutil.which("btop") is not None

    def run(self):
        if not self.is_available():
            return False

        try:
            result = subprocess.run(
                ["btop"],
                check=False,
            )
            return result.returncode == 0

        except OSError:
            return False
