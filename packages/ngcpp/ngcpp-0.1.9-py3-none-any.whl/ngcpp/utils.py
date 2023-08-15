from subprocess import PIPE, Popen

import pandas as pd

LOG_FORMAT = (
    "[<green>{time:MM-DD HH:mm:ss}</green>|"
    "<red>{process.name}</red>|"
    "<level>{level: <8}</level>|"
    "<cyan>{file.path}</cyan>:<cyan>{line}</cyan>:<cyan>{function}</cyan>]"
    "<level>{message}</level>"
)


def run_simple_command(cmd: str):
    # cmd = cmd.split(" ")
    with Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE) as prc:
        stdout, stderr = prc.communicate()
        if stdout:
            stdout = stdout.decode("utf-8")
        if stderr:
            stderr = stderr.decode("utf-8")
        prc.terminate()
    return stdout, stderr


def parse_duration(duration):
    if pd.isnull(duration) or duration == "-":
        return 0
    if "day" in duration:
        days, time = duration.split(", ")
        days = int(days.split(" ")[0])
        hours, minutes, seconds = map(int, time.split(":"))
        total_seconds = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
    else:
        hours, minutes, seconds = map(int, duration.split(":"))
        total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds / 3600
