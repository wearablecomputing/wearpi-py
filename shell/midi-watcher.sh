#!/bin/bash
#
# MIDI watcher: keeps the EAVI biosignal board (BLE-MIDI, Bluetooth name
# OWL-BioSignals-P010) routed into Pd's MIDI input for the whole session.
#
# Started in the background by startup.sh. Every second it tries to
# connect the EAVI's ALSA MIDI port to Pd's. aconnect only succeeds when
# both ports exist and are not yet connected, so:
#   - EAVI or Pd missing   -> fails silently, retry later
#   - already connected    -> fails silently ("already subscribed")
#   - both present, unlinked (e.g. after the EAVI dropped out and BlueZ
#     reconnected it, or Pd restarted) -> connects and logs a line
# Ports are matched by name because ALSA client numbers can change. The
# EAVI's port is normally named after its advertised name, but after
# pairing it has also reported its internal GAP name "bluenrg", so both
# names are tried.
#
# The EAVI only sends MIDI over an encrypted link, i.e. it must be bonded
# (paired with its passkey). If the bond is lost (e.g. the EAVI was paired
# with another computer and forgot the Pi's keys), it still shows up as
# connected with a MIDI port, but no data arrives and the link drops every
# ~30s. After each connect the watcher checks for this and logs a warning.
#
# Log: /tmp/midi-watcher.log (timestamped reconnect history; cleared on reboot)

SRCS=('OWL-BioSignals-P010:0' 'bluenrg:0')
DST='Pure Data:0'
EAVI_MAC='E2:16:01:30:31:30'
INTERVAL=1
LOG=/tmp/midi-watcher.log

log() {
    echo "$(date '+%F %T') $*" >> "$LOG"
}

log "watcher started (${SRCS[*]} -> $DST, every ${INTERVAL}s)"

while true; do
    for src in "${SRCS[@]}"; do
        if aconnect "$src" "$DST" 2>/dev/null; then
            log "connected $src -> $DST"
            if ! bluetoothctl info "$EAVI_MAC" 2>/dev/null | grep -q 'Bonded: yes'; then
                log "WARNING: EAVI connected but not bonded - no MIDI will arrive." \
                    "Re-pair it with its passkey (bluetoothctl: remove, pair, trust, connect)."
            fi
            break
        fi
    done
    sleep "$INTERVAL"
done
