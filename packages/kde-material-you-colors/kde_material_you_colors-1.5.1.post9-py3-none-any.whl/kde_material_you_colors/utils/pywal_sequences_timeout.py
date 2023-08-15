"""
Send sequences to all open terminals.
Original file from pywal but changed to send sequences only to active ttys

Inspired by by @havulv https://github.com/dylanaraps/pywal/pull/598

Unfortunatelly their approach didn't work as some ttys like kitty wont show in
`who` but on `who -d` (dead) command so I resorted to using threads instead
to stop the write if it takes more than a second
"""
import glob
import logging
import os
import subprocess
import threading
from pywal.settings import CACHE_DIR, OS
from pywal import util


def sequences_send_worker(sequences, dev, stop_event):
    if not stop_event.is_set():
        util.save_file(sequences, dev)


def set_special(index, color, iterm_name="h", alpha=100):
    """Convert a hex color to a special sequence."""
    if OS == "Darwin" and iterm_name:
        return "\033]P%s%s\033\\" % (iterm_name, color.strip("#"))

    if index in [11, 708] and alpha != "100":
        return "\033]%s;[%s]%s\033\\" % (index, alpha, color)

    return "\033]%s;%s\033\\" % (index, color)


def set_color(index, color):
    """Convert a hex color to a text color sequence."""
    if OS == "Darwin" and index < 20:
        return "\033]P%1x%s\033\\" % (index, color.strip("#"))

    return "\033]4;%s;%s\033\\" % (index, color)


def set_iterm_tab_color(color):
    """Set iTerm2 tab/window color"""
    return (
        "\033]6;1;bg;red;brightness;%s\a"
        "\033]6;1;bg;green;brightness;%s\a"
        "\033]6;1;bg;blue;brightness;%s\a"
    ) % (*util.hex_to_rgb(color),)


def create_sequences(colors, vte_fix=False):
    """Create the escape sequences."""
    alpha = colors["alpha"]

    # Colors 0-15.
    sequences = [
        set_color(index, colors["colors"]["color%s" % index]) for index in range(16)
    ]

    # Special colors.
    # Source: https://goo.gl/KcoQgP
    # 10 = foreground, 11 = background, 12 = cursor foreground
    # 13 = mouse foreground, 708 = background border color.
    sequences.extend(
        [
            set_special(10, colors["special"]["foreground"], "g"),
            set_special(11, colors["special"]["background"], "h", alpha),
            set_special(12, colors["special"]["cursor"], "l"),
            set_special(13, colors["special"]["foreground"], "j"),
            set_special(17, colors["special"]["foreground"], "k"),
            set_special(19, colors["special"]["background"], "m"),
            set_color(232, colors["special"]["background"]),
            set_color(256, colors["special"]["foreground"]),
            set_color(257, colors["special"]["background"]),
        ]
    )

    if not vte_fix:
        sequences.extend(set_special(708, colors["special"]["background"], "", alpha))

    if OS == "Darwin":
        sequences += set_iterm_tab_color(colors["special"]["background"])

    return "".join(sequences)


def send(colors, cache_dir=CACHE_DIR, to_send=True, vte_fix=False):
    """Send colors to all open terminals."""
    if OS == "Darwin":
        devices = glob.glob("/dev/ttys00[0-9]*")
    elif OS == "OpenBSD":
        devices = subprocess.check_output(
            "ps -o tty | sed -e 1d -e s#^#/dev/# | sort | uniq",
            shell=True,
            universal_newlines=True,
        ).split()
    else:
        devices = glob.glob("/dev/pts/[0-9]*")

    sequences = create_sequences(colors, vte_fix)

    # Send data to active terminal devices.
    logging.debug("Sending sequences to %s", " ".join(devices))
    if to_send:
        for dev in devices:
            stop_event = threading.Event()

            t = threading.Thread(
                target=sequences_send_worker, args=[sequences, dev, stop_event]
            )
            t.start()
            t.join(timeout=1)
            if t.is_alive():
                logging.warning("%s was taking too long to respond, stopping", dev)
                stop_event.set()

    util.save_file(sequences, os.path.join(cache_dir, "sequences"))
    logging.info("Set terminal colors.")
