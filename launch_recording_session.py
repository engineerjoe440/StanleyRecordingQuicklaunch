################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

import subprocess
import time
from pathlib import Path

from pipewire_python import link as pw


REAPER_TEMPLATE = "DualChannelRecording.RPP"
TEMPLATE_PATH = Path("~/.config/REAPER/ProjectTemplates/").expanduser()

REAPER_DEVICE_NAME = "REAPER"

ANALOG_INPUT_DEVICE_NAME = "alsa_input.usb-Burr-Brown_from_TI_USB_Audio_CODEC-00.analog-stereo-input"


def launch_reaper():
    """Launch the Reaper Application with the Appropriate Template."""
    subprocess.Popen([
        "reaper",
        "-template",
        str(TEMPLATE_PATH.joinpath(REAPER_TEMPLATE)),
    ])


class PipeWireSession:
    """Management Interface to Control the PipeWire Session."""

    def __init__(self):
        """Load PipeWire Link Information."""
        self.reaper_device_left = None
        self.reaper_device_right = None
        self.disconnect_default_connections()
        self.connect_analog_input()

    def disconnect_default_connections(self):
        """Disconnect the Default Reaper Connections"""
        for link_group in pw.list_link_groups():
            if link_group.common_device == REAPER_DEVICE_NAME:
                for link in link_group.links:
                    if link.input.device == REAPER_DEVICE_NAME:
                        # Disconnect Existing Links
                        link.disconnect()
                        # Track the REAPER Interface
                        if "FR" in link_group.common_name.upper():
                            self.reaper_device_right = link.input
                        if "FL" in link_group.common_name.upper():
                            self.reaper_device_left = link.input
        # Confirm Reaper Connections were Found
        if self.reaper_device_left is None or self.reaper_device_right is None:
            raise ValueError("Cannot Locate Reaper Interface.")
        
    def connect_analog_input(self):
        """Connect the Analog Input."""
        analog_left = pw.Output(
            device=ANALOG_INPUT_DEVICE_NAME,
            name="capture_FL",
            id=0,
            port_type=pw.PortType.OUTPUT
        )
        analog_right = pw.Output(
            device=ANALOG_INPUT_DEVICE_NAME,
            name="capture_FR",
            id=0,
            port_type=pw.PortType.OUTPUT
        )
        analog_left.connect(self.reaper_device_left)
        analog_right.connect(self.reaper_device_left)


if __name__ == "__main__":
    launch_reaper()
    time.sleep(5)
    session = PipeWireSession()
