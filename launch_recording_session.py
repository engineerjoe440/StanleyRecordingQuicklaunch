################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

import subprocess
import time
from pathlib import Path

import pulsectl

from configure_routes import PipeWireSession


REAPER_TEMPLATE = "MultiChannelRecording.RPP"
TEMPLATE_PATH = Path("~/.config/REAPER/ProjectTemplates/").expanduser()

SOUNDUX_SCRIPT_PATH = (
    "/home/joestan/stanleypadconfig/StreamDeck/launch_soundux.sh"
)

REMOTE_VOLUME = 0.74


def launch_reaper():
    """Launch the Reaper Application with the Appropriate Template."""
    subprocess.Popen([
        "pw-jack", # Use Pipewire Jack
        "reaper",
        "-template",
        str(TEMPLATE_PATH.joinpath(REAPER_TEMPLATE)),
    ])

def launch_soundux():
    """Launch the Soundux Application."""
    subprocess.Popen([SOUNDUX_SCRIPT_PATH])

def launch_easy_effects():
    """Launch the Easy Effects Audio Application."""
    subprocess.Popen(["easyeffects",])

def set_audio_levels():
    """Shut down Recording System."""
    with pulsectl.Pulse('manager') as pulse:
        for stream in pulse.sink_input_list():
            if stream.name == "Playback":
                pulse.volume_set_all_chans(stream, REMOTE_VOLUME)


if __name__ == "__main__":
    launch_soundux()
    launch_easy_effects()
    set_audio_levels()
    launch_reaper()
    time.sleep(5)
    session = PipeWireSession()
