import shutil
import subprocess


class Fastfetch:

    def is_available(self):
        return shutil.which("fastfetch") is not None

    def run(self):
        if not self.is_available():
            return False

        try:
            subprocess.run(
                ["fastfetch"],
                check=False,
            )
            return True

        except OSError:
            return False