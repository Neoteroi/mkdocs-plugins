import logging
import subprocess

logger = logging.getLogger("MARKDOWN")


class Command:
    def __init__(self, command: str):
        self._command = None
        self.command = command

    @property
    def command(self):
        if not self._command:
            raise TypeError("Missing command")
        return self._command

    @command.setter
    def command(self, value):
        self._command = value

    def execute(self) -> str:
        logger.debug(f"\nNeoteroi Contrib; executing command:\n  {self.command}\n")
        p = subprocess.Popen(
            self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if p.stdout is None:
            raise TypeError("Missing subprocess stdout")

        output = p.stdout.read()
        error_output = p.stderr.read() if p.stderr else None

        try:
            output = output.decode("utf8")
        except UnicodeDecodeError:
            output = output.decode("ISO-8859-1")

        if error_output:
            raise RuntimeError(
                f"Process failed with return code: "
                f"{p.returncode}.\nOutput: {output}"
            )

        if p.returncode is not None and p.returncode != 0:
            raise RuntimeError(
                f"Process failed with return code: "
                f"{p.returncode}.\nOutput: {output}"
            )

        if output:
            logger.debug(f"Neoteroi Contrib; got output:\n  {output}\n")
        return output
