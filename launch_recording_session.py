################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

import subprocess
from pathlib import Path

from pipewire_python import link as pw
from pipewire_python.link import StereoInput


REAPER_TEMPLATE = "DualChannelRecording.RPP"
TEMPLATE_PATH = Path("~/.config/REAPER/ProjectTemplates/").expanduser()

REAPER_DEVICE_NAME = "REAPER"


def launch_reaper():
    """Launch the Reaper Application with the Appropriate Template."""
    args = [
        "reaper",
        "-template",
        str(TEMPLATE_PATH.joinpath(REAPER_TEMPLATE))
    ]
    status = subprocess.Popen(args)


class PipeWireSession:
    """Management Interface to Control the PipeWire Session."""

    def __init__(self):
        """Load PipeWire Link Information."""
        for link in pw.list_links():
            if link.input.device == REAPER_DEVICE_NAME:
                pass