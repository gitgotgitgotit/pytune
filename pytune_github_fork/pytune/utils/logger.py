"""Consistent, colorized terminal logging for Pytune."""
from datetime import datetime, timezone

from rich.console import Console
from rich.text import Text


class Logger:
    LEVELS = {
        "alert": ("!", "bold yellow"),
        "debug": ("*", "dim"),
        "info": ("i", "bold blue"),
        "success": ("+", "bold green"),
        "warning": ("!", "bold orange3"),
        "error": ("x", "bold red"),
        # Domain labels requested for consistent visual distinction.
        "certificate": ("CERT", "bold green"),
        "auth": ("AUTH", "bold yellow"),
        "settings": ("CFG", "bold magenta"),
        "file": ("FILE", "bold cyan"),
    }

    def __init__(self, verbose=False, quiet=False, console=None):
        self.verbose = verbose
        self.quiet = quiet
        self.console = console or Console(stderr=False)

    def _log(self, level, message, *, force=False):
        if self.quiet and not force:
            return
        if level == "debug" and not self.verbose:
            return

        label, style = self.LEVELS[level]
        timestamp = datetime.now(timezone.utc).astimezone().strftime("%H:%M:%S")
        line = Text()
        line.append(f"{timestamp} ", style="dim")
        line.append(f"[{label}] ", style=style)
        # Rich escapes markup in Text, so arbitrary messages are printed literally.
        line.append(str(message))
        self.console.print(line, highlight=False)

    def alert(self, message):
        self._log("alert", message)

    def debug(self, message):
        self._log("debug", message)

    def info(self, message):
        self._log("info", message)

    def success(self, message):
        self._log("success", message)

    def warning(self, message):
        self._log("warning", message)

    def error(self, message):
        # Errors remain visible in quiet mode: hiding failures is misleading.
        self._log("error", message, force=True)

    def certificate(self, message):
        self._log("certificate", message)

    def auth(self, message):
        self._log("auth", message)

    def settings(self, message):
        self._log("settings", message)

    def file(self, message):
        self._log("file", message)
