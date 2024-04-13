################################################################################
"""
Start a new Reaper recording session with the appropriate PipeWire Configuration
"""
################################################################################

from pipewire_python import link as pw

REAPER_DEVICE_NAME = "REAPER"

ANALOG_INPUT_DEVICE_NAME = "alsa_input.usb-BurrBrown_from_Texas_Instruments_USB_AUDIO_CODEC-00.analog-stereo"
ANALOG_OUTPUT_DEVICE_NAME = "alsa_output.usb-BurrBrown_from_Texas_Instruments_USB_AUDIO_CODEC-00.analog-stereo"
EASY_EFFECTS_INPUT_DEVICE_NAME = "easyeffects_sink"
EASY_EFFECTS_OUTPUT_DEVICE_NAME = "ee_soe_output_level"
SOUNDUX_SINK_OUTPUT_DEVICE_NAME = "soundux_sink"
ZOOM_DEVICE_NAME = "ZOOM VoiceEngine"


class PipeWireSession:
    """Management Interface to Control the PipeWire Session."""

    def __init__(self):
        """Load PipeWire Link Information."""
        self.num_reaper_inputs = 4
        self.reaper_devices = [None] * self.num_reaper_inputs
        self.zoom_output_left = None
        self.zoom_output_right = None
        self.digital_left = None
        self.digital_right = None
        self.disconnect_default_connections()
        self.connect_analog_input()
        self.connect_digital_input()
        self.connect_easy_effects_zoom()
        self.connect_easy_effects_output()
        self.connect_soundux_input()

    def disconnect_default_connections(self):
        """Disconnect the Default Reaper and Zoom Connections."""
        for link_group in pw.list_link_groups():
            if link_group.common_device == REAPER_DEVICE_NAME:
                for link in link_group.links:
                    if link.input.device == REAPER_DEVICE_NAME:
                        # Disconnect Existing Links
                        link.disconnect()
                        # Track the REAPER Interface
                        for input_idx in range(self.num_reaper_inputs):
                            if link_group.common_name == f"in{input_idx + 1}":
                                self.reaper_devices[input_idx] = link.input
            if link_group.common_device == ZOOM_DEVICE_NAME:
                for link in link_group.links:
                    if link.output.device == ZOOM_DEVICE_NAME:
                        # Disconnect Existing Links
                        link.disconnect()
                        # Track the Zoom Interface
                        if "FR" in link_group.common_name.upper():
                            self.zoom_output_right = link.output
                        if "FL" in link_group.common_name.upper():
                            self.zoom_output_left = link.output
            if link_group.common_device == EASY_EFFECTS_OUTPUT_DEVICE_NAME:
                for link in link_group.links:
                    if link.output.device == EASY_EFFECTS_OUTPUT_DEVICE_NAME:
                        # Disconnect Existing Links
                        link.disconnect()
                        # Track the Digital Out Interface
                        if "FR" in link_group.common_name.upper():
                            self.digital_right = link.output
                        if "FL" in link_group.common_name.upper():
                            self.digital_left = link.output
        # Confirm Reaper Connections were Found
        if not any(self.reaper_devices):
            raise ValueError("Cannot Locate Reaper Interface.")

    def connect_analog_input(self):
        """Connect the Analog Input."""
        reaper_port = self.reaper_devices[0] or pw.Input(
            device=REAPER_DEVICE_NAME,
            name="in1",
            id=0,
            port_type=pw.PortType.INPUT
        )
        pw.Output(
            device=ANALOG_INPUT_DEVICE_NAME,
            name="capture_FL",
            id=0,
            port_type=pw.PortType.OUTPUT
        ).connect(reaper_port)
        pw.Output(
            device=ANALOG_INPUT_DEVICE_NAME,
            name="capture_FR",
            id=0,
            port_type=pw.PortType.OUTPUT
        ).connect(reaper_port)

    def connect_digital_input(self):
        """Connect the Digital Input."""
        try:
            reaper_port = self.reaper_devices[1] or pw.Input(
                device=REAPER_DEVICE_NAME,
                name="in2",
                id=0,
                port_type=pw.PortType.INPUT
            )
            self.digital_left.connect(reaper_port)
            self.digital_right.connect(reaper_port)
        except AttributeError:
            print("WARNING: Failed to connect Digital Input.")

    def connect_soundux_input(self):
        """Connect the Soundux Interface."""
        reaper_port = self.reaper_devices[2] or pw.Input(
            device=REAPER_DEVICE_NAME,
            name="in3",
            id=0,
            port_type=pw.PortType.INPUT
        )
        pw.Output(
            device=SOUNDUX_SINK_OUTPUT_DEVICE_NAME,
            name="monitor_FL",
            id=0,
            port_type=pw.PortType.OUTPUT
        ).connect(reaper_port)
        pw.Output(
            device=SOUNDUX_SINK_OUTPUT_DEVICE_NAME,
            name="monitor_FR",
            id=0,
            port_type=pw.PortType.OUTPUT
        ).connect(reaper_port)

    def connect_easy_effects_zoom(self):
        """Connect the Zoom Output to Easy Effects if Zoom is Already Started."""
        try:
            if self.zoom_output_left is None or self.zoom_output_right is None:
                return
            easy_effects_left = pw.Input(
                device=EASY_EFFECTS_INPUT_DEVICE_NAME,
                name="playback_FL",
                id=0,
                port_type=pw.PortType.INPUT
            )
            easy_effects_right = pw.Input(
                device=EASY_EFFECTS_INPUT_DEVICE_NAME,
                name="playback_FR",
                id=0,
                port_type=pw.PortType.INPUT
            )
            easy_effects_left.connect(self.zoom_output_left)
            easy_effects_right.connect(self.zoom_output_right)
        except AttributeError:
            print("WARNING: Failed to connect Easy Effects to Zoom.")

    def connect_easy_effects_output(self):
        """Connect the Easy Effects Output to the Appropriate DAC."""
        try:
            analog_output_left = pw.Input(
                device=ANALOG_OUTPUT_DEVICE_NAME,
                name="playback_FL",
                id=0,
                port_type=pw.PortType.INPUT
            )
            analog_output_right = pw.Input(
                device=ANALOG_OUTPUT_DEVICE_NAME,
                name="playback_FR",
                id=0,
                port_type=pw.PortType.INPUT
            )
            analog_output_left.connect(self.digital_left)
            analog_output_right.connect(self.digital_right)
        except AttributeError:
            print("WARNING: Failed to connect Easy Effects to Zoom.")


if __name__ == "__main__":
    session = PipeWireSession()
