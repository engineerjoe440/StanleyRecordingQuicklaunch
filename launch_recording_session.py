################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

import subprocess
import time
from pathlib import Path

from configure_routes import PipeWireSession


REAPER_TEMPLATE = "MultiChannelRecording.RPP"
TEMPLATE_PATH = Path("~/.config/REAPER/ProjectTemplates/").expanduser()


def launch_reaper():
    """Launch the Reaper Application with the Appropriate Template."""
    subprocess.Popen([
        "pw-jack", # Use Pipewire Jack
        "reaper",
        "-template",
        str(TEMPLATE_PATH.joinpath(REAPER_TEMPLATE)),
    ])

def launch_easy_effects():
    """Launch the Easy Effects Audio Application."""
    subprocess.Popen(["easyeffects",])


if __name__ == "__main__":
    launch_easy_effects()
    launch_reaper()
    time.sleep(5)
    session = PipeWireSession()
