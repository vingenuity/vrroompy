#!/usr/bin/env python3

"""
Contains enumeration classes that are used across multiple commands.
"""

from enum import Enum


class OnOffSwitch(Enum):
    """
    Enumerates the values for a VRROOM on/off switch.
    """

    OFF = "off"
    ON = "on"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_bool(on: bool) -> "OnOffSwitch":
        """
        Converts a boolean into a value of this enumeration, if possible.
        """
        if on:
            return OnOffSwitch.ON
        return OnOffSwitch.OFF

    @staticmethod
    def from_string(string: str) -> "OnOffSwitch":
        """
        Converts a string into a value of this enumeration, if possible.
        """
        return OnOffSwitch(string)

    @staticmethod
    def pattern() -> str:
        """
        Returns a regex pattern that matches values of this enumeration.
        """
        return f"(?:{OnOffSwitch.OFF}|{OnOffSwitch.ON})"

    @staticmethod
    def to_bool(on_off: "OnOffSwitch") -> bool:
        """
        Converts a string to a bool via this enumeration, if possible.
        """
        if on_off == OnOffSwitch.ON:
            return True
        return False


class Target(Enum):
    """
    Enumerates the valid targets for VRROOM commands.

    Targets are defined in the order they are specified in the documentation.
    """

    # Modes
    OPERATION_MODE = "opmode"

    # Inputs
    SELECTED_INPUTS = "insel"
    SELECTED_INPUT_TX0 = "inseltx0"
    SELECTED_INPUT_TX1 = "inseltx1"

    # Network
    IP_ADDRESS = "ipaddr"
    IP_NETWORK_MASK = "ipmask"
    IP_GATEWAY = "ipgw"
    DHCP_ENABLED = "dhcp"
    IP_INTERRUPTS_ENABLED = "ipinterrupt"
    TCP_PORT = "tcpport"

    # Modes
    AUTO_SWITCHING = "autosw"

    # EDID
    EDID_MODE = "edidmode"
    EDID_AUDIO = "edid audio"
    EDID_VIDEO = "edid video"
    EDID_FRL_AUTOMIX = "edidfrlflag"
    EDID_FRL_MODE = "edidfrlmode"
    EDID_VRR_AUTOMIX = "edidvrrflag"
    EDID_VRR_MODE = "edidvrrmode"
    EDID_ALLM_AUTOMIX = "edidallmflag"
    EDID_ALLM_MODE = "edidallmmode"
    EDID_HDR_AUTOMIX = "edidhdrflag"
    EDID_HDR_MODE = "edidhdrmode"
    EDID_DVF_AUTOMIX = "ediddvflag"
    EDID_DV_MODE = "ediddvmode"
    EDID_PCM_AUTOMIX = "edidpcmflag"
    EDID_PCM_CHANNEL_COUNT = "edidpcmchmode"
    EDID_PCM_SAMPLE_RATE = "edidpcmsrmode"
    EDID_PCM_BIT_WIDTH = "edidpcmbwmode"
    EDID_TRUEHD_AUTOMIX = "edidtruehdflag"
    EDID_TRUEHD_MODE = "edidtruehdmode"
    EDID_TRUEHD_SAMPLE_RATE = "edidtruehdsrmode"
    EDID_DD_AUTOMIX = "edidddflag"
    EDID_DD_MODE = "edidddmode"
    EDID_DD_PLUS_AUTOMIX = "edidddplusflag"
    EDID_DD_PLUS_MODE = "edidddplusmode"
    EDID_DD_PLUS_SAMPLE_RATE = "edidddplussrmode"
    EDID_DTS_AUTOMIX = "ediddtsflag"
    EDID_DTS_MODE = "ediddtsmode"
    EDID_DTS_HD_AUTOMIX = "ediddtshdflag"
    EDID_DTS_HD_MODE = "ediddtshdmode"
    EDID_DTS_HD_SAMPLE_RATE = "ediddtshdsrmode"
    EDID_ONE_BIT_AUDIO_AUTOMIX = "edidonebitflag"
    EDID_ONE_BIT_AUDIO_MODE = "edidonebitmode"

    # Modes
    HDCP_MODE = "hdcp"

    # EDID
    EDID_TABLE_RX0 = "edidtableinp0"
    EDID_TABLE_RX1 = "edidtableinp1"
    EDID_TABLE_RX2 = "edidtableinp2"
    EDID_TABLE_RX3 = "edidtableinp3"

    # Video
    HDR_CUSTOM = "hdrcustom"
    HDR_CUSTOM_HDR10 = "hdrcustomhdr10only"
    HDR_CUSTOM_HLG = "hdrcustomhlgonly"
    HDR_CUSTOM_HLG_AUTO = "hdrcustomhlgonlyauto"
    HDR_DISABLE = "hdrdisable"
    HDR_DISABLE_HDR10 = "hdrdisablehdr10only"
    HDR_DISABLE_HLG = "hdrdisablehlgonly"
    AVI_INFOFRAME_CUSTOM = "avicustom"
    AVI_INFOFRAME_DISABLE = "avidisable"

    # CEC
    CEC = "cec"
    CEC_ADDRESS = "cecla"

    # OLED
    OLED = "oled"
    OLED_PAGE = "oledpage"
    OLED_FADE_TIME = "oledfade"

    # Audio
    HDMI_MUTED_TX0 = "mutetx0audio"
    HDMI_MUTED_TX1 = "mutetx1audio"
    ANALOG_VOLUME = "analogvolume"
    ANALOG_BASS = "analogbass"
    ANALOG_TREBLE = "analogtreble"

    # Actions
    ACTION_REBOOT = "reboot"
    ACTION_FACTORY_RESET = "factoryreset"

    # JVC Macros
    JVC_MACRO_ENABLED = "jvcmacro"
    JVC_MACRO_ON_SYNC = "jvcmacrosync"
    JVC_MACRO_DELAY = "jvcmacrodelay"
    JVC_MACRO_MODE_HDR = "jvcmacrohdr10mode"
    JVC_MACRO_HEX_ENABLED = "jvcmacroalwayshex"
    JVC_MACRO_HEX_ORDER = "jvcmacroalwayshexorder"
    JVC_MACRO_HEX_DELAY = "jvcmacroalwayshexdelay"

    # Voltage
    VOLTAGE_PLUS5_ENABLED_TX0 = "tx0plus5"
    VOLTAGE_PLUS5_ENABLED_TX1 = "tx1plus5"

    # Modes
    EARC_MODE = "earcforce"
    HTPC_MODE_ENABLED_RX0 = "htpcmode0"
    HTPC_MODE_ENABLED_RX1 = "htpcmode1"
    HTPC_MODE_ENABLED_RX2 = "htpcmode2"
    HTPC_MODE_ENABLED_RX3 = "htpcmode3"

    # Status
    STATUS = "status"

    # Audio
    LPCM_CHANNEL_COUNT_TX0 = "audiochtx0"
    LPCM_CHANNEL_COUNT_TX1 = "audiochtx1"
    LPCM_CHANNEL_COUNT_OUT = "audiochaudout"
    LPCM_MODE_TX0 = "audiomodetx0"
    LPCM_MODE_TX1 = "audiomodetx1"
    LPCM_MODE_OUT = "audiomodeaudout"

    # EDID
    EDID_TABLE = "edidtable"

    # Actions
    ACTION_HOTPLUG = "hotplug"

    # CDS
    CDS_STRING = "cdsstr"

    def __str__(self) -> str:
        return str(self.value)

    @staticmethod
    def from_string(string: str) -> "Target":
        """
        Converts a string into a value of this enumeration, if possible.
        """
        return Target(string)

    @staticmethod
    def is_valid(target_name: str) -> bool:
        """
        Returns whether the named target is valid for use in VRROOM commands.
        """
        try:
            Target(target_name)
        except ValueError:
            return False
        return True
