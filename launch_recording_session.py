#!./venv/bin/python3
################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

import re
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

def find_process(process_name: str):
    """Find the Process in the System Output."""
    with subprocess.Popen(
        f"ps -eaf | grep {process_name}",
        shell=True,
        encoding='utf8',
        stdout=subprocess.PIPE,
    ) as proc:
        output = proc.stdout.read()

    return output

def is_proc_running(process_name: str):
    """Check if the Process is Running."""
    output = find_process(process_name)

    return bool(re.search(process_name, output))

if __name__ == "__main__":
    launch_soundux()
    launch_easy_effects()
    set_audio_levels()
    launch_reaper()
    while not is_proc_running(process_name="reaper"):
        time.sleep(2)
    time.sleep(15)
    session = PipeWireSession()
