
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

import psutil


class SystemInfo:

    @property
    def os_name(self):
        try:
            data = Path("/etc/os-release").read_text()
            match = re.search(r'^PRETTY_NAME="?([^"\n]+)', data, re.M)
            if match:
                return match.group(1)
        except OSError:
            pass

        return platform.system()

    @property
    def kernel(self):
        return platform.release()

    @property
    def architecture(self):
        return platform.machine()

    @property
    def hostname(self):
        return platform.node()

    @property
    def shell(self):
        shell = os.environ.get("SHELL")
        return Path(shell).name if shell else "Неизвестно"

    @property
    def terminal(self):
        # TERM описывает возможности терминала, а не всегда его название.
        return (
            os.environ.get("TERM_PROGRAM")
            or os.environ.get("TERMINAL")
            or os.environ.get("TERM")
            or "Неизвестно"
        )

    @property
    def desktop(self):
        return (
            os.environ.get("XDG_CURRENT_DESKTOP")
            or os.environ.get("XDG_SESSION_DESKTOP")
            or "Неизвестно"
        )

    @property
    def cpu(self):
        try:
            for line in Path("/proc/cpuinfo").read_text().splitlines():
                if line.startswith("model name"):
                    return line.split(":", 1)[1].strip()
        except OSError:
            pass

        return platform.processor() or "Неизвестно"

    @property
    def gpu(self):
        if not shutil.which("lspci"):
            return "Неизвестно (нужен pciutils)"

        try:
            result = subprocess.run(
                ["lspci"],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )

            for line in result.stdout.splitlines():
                if re.search(r"VGA compatible controller|3D controller|Display controller",
                             line, re.I):
                    return line.split(": ", 1)[-1].strip()

        except (OSError, subprocess.TimeoutExpired):
            pass

        return "Неизвестно"

    @property
    def uptime(self):
        seconds = int(max(0, psutil.time.time() - psutil.boot_time()))

        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        return (
            f"{days} дн. {hours:02} ч. "
            f"{minutes:02} мин. {seconds:02} сек."
        )
