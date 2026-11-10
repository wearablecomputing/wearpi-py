#!/bin/bash
#
# MIDI watcher: keeps the OWL-BioSignals-P010 EMG board (BLE-MIDI) routed
# into Pd's MIDI input for the whole session.
#
# Started in the background by startup.sh. Every second it tries to
# connect the board's ALSA MIDI port to Pd's. aconnect only succeeds when
# both ports exist and are not yet connected, so:
#   - board or Pd missing  -> fails silently, retry later
#   - already connected    -> fails silently ("already subscribed")
#   - both present, unlinked (e.g. after the board dropped out and BlueZ
#     reconnected it, or Pd restarted) -> connects and logs a line
# Ports are matched by name because ALSA client numbers can change.
#
# Log: /tmp/midi-watcher.log (timestamped reconnect history; cleared on reboot)

SRC='OWL-BioSignals-P010:0'
DST='Pure Data:0'
INTERVAL=1
LOG=/tmp/midi-watcher.log

echo "$(date '+%F %T') watcher started ($SRC -> $DST, every ${INTERVAL}s)" >> "$LOG"

while true; do
    if aconnect "$SRC" "$DST" 2>/dev/null; then
        echo "$(date '+%F %T') connected $SRC -> $DST" >> "$LOG"
    fi
    sleep "$INTERVAL"
done
