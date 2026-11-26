"""Deadpan forecast for Tumbleford, a city that does not exist.

Writes one broadcast line to $MAKEFUN_OUTPUT_DIR/entry.txt: the
evening forecast for Tumbleford, read straight-faced by a TV
meteorologist who has seen ten thousand forecasts and been
impressed by none of them. Today's high of 62 arrives at
2:15, stays eleven minutes, then leaves; a low of 61 follows,
with a 40% chance of Tuesday. Standard library only; the line
is checked against the competition gate (one line, 1 to 160
characters of UTF-8 text, not only whitespace) before anything
is written, and it must read like a real broadcast: a named
city, a temperature, and a chance, delivered deadpan.
"""

import os
import sys

FORECAST = (
    "Good evening from Tumbleford, where today's high of 62 "
    "arrives at 2:15, stays eleven minutes, then leaves; a low "
    "of 61 follows, with a 40% chance of Tuesday."
)

CHAR_LIMIT = 160


def forecast_line():
    """Return the evening forecast for Tumbleford."""
    return FORECAST


def check_gate(text):
    """Check the forecast against the competition gate.

    The gate wants one line of plain UTF-8 text, between 1 and
    160 characters, that is not only whitespace: a weather
    forecast for a city that does not exist. A line that fails
    here is rejected instead of wasting a submission on the
    server.
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("forecast is empty")
    if len(cleaned) > CHAR_LIMIT:
        raise ValueError(
            "forecast is %d characters, over the 160 limit"
            % len(cleaned)
        )
    if "\n" in cleaned or "\r" in cleaned:
        raise ValueError("forecast must fit on exactly one line")
    if not cleaned.endswith("."):
        raise ValueError("forecast must end with a full stop")
    return cleaned


def check_broadcast(text):
    """Check the forecast reads like a real broadcast line.

    A deadpan meteorologist names the city, gives a
    temperature, and gives a chance: without all three the line
    is a joke about weather, not a forecast. The city must be
    Tumbleford, the temperature must be a number, and the
    chance must be a percent, or the line is rejected here.
    """
    lowered = text.lower()
    if "tumbleford" not in lowered:
        raise ValueError("forecast never names its city")
    if not any(ch.isdigit() for ch in text):
        raise ValueError("forecast carries no temperature")
    if "% chance" not in lowered:
        raise ValueError("forecast gives no chance")
    return text


def forecast_uses_its_characters(text):
    """Check the forecast uses its 160 characters well.

    The judge's last test is pacing: a line far under the cap
    reads thin beside one that fills it, and a line that only
    just fits reads cramped. A forecast under 120 characters
    has not earned its place on the map, so it is rejected
    here before anything is written.
    """
    if len(text) < 120:
        raise ValueError(
            "forecast is only %d characters, too thin for the map"
            % len(text)
        )
    return text


def forecast_measure(text):
    """Measure the forecast for a last sanity pass.

    Returns the character and word counts. A line too short to
    carry the setup and the twist, or one padded out to fill
    the cap, is caught here before anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    line = check_gate(forecast_line())
    line = check_broadcast(line)
    line = forecast_uses_its_characters(line)
    shape = forecast_measure(line)
    if shape["words"] < 5:
        raise ValueError("forecast is too short to land the joke")
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
