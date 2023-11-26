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
        analog_left.connect(self.reaper_devices[0])
        analog_right.connect(self.reaper_devices[0])

    def connect_digital_input(self):
        """Connect the Digital Input."""
        self.digital_left.connect(self.reaper_devices[1])
        self.digital_right.connect(self.reaper_devices[1])

    def connect_easy_effects_zoom(self):
        """Connect the Zoom Output to Easy Effects if Zoom is Already Started."""
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

    def connect_easy_effects_output(self):
        """Connect the Easy Effects Output to the Appropriate DAC."""
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


if __name__ == "__main__":
    session = PipeWireSession()
