################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

import subprocess
from pathlib import Path

from pipewire_python import link as pw


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
        self.reaper_device = None
        for link in pw.list_links():
            for input_device in link.inputs:
                if input_device.device == REAPER_DEVICE_NAME:
                    # Track the REAPER Interface
                    link.disconnect()
                    self.reaper_device = input_device
        if self.reaper_device is None:
            raise ValueError("Cannot Locate Reaper Interface.")
        print(self.reaper_device)


if __name__ == "__main__":
    launch_reaper()
    session = PipeWireSession()
