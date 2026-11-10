#!/bin/bash

# Kill any stale instances before launching.
# Patterns are anchored/exact so they only hit the real processes, not any
# other command whose arguments happen to mention these names.
# Python scripts: match the interpreter + script path at the start of the command line.
pkill -f '^/home/wearpi/env/bin/python3 /home/wearpi/git/wearpi-py/wearpi-osc-lists' 2>/dev/null
# Pd: exact process name, "puredata" when started here, "pd" when opened via the GUI.
pkill -x 'puredata|pd' 2>/dev/null
# MIDI watcher: exact process name.
pkill -x midi-watcher.sh 2>/dev/null
sleep 1

# Navigate to your project directory (adjust as needed)
cd /home/wearpi/git/wearpi-py

# Run a command in the background, logging its output and how it ended.
# Usage: run_logged <logfile> <command> [args...]
# Appends to <logfile>: a timestamped start line, everything the command prints
# (stdout and stderr, e.g. Python tracebacks), and a timestamped exit line with
# the exit code. If the process was killed by a signal (e.g. 132 = SIGILL
# "Illegal instruction", 139 = SIGSEGV, 137 = SIGKILL from the OOM killer,
# 143 = SIGTERM from the pkill above) the signal name is added, since Python
# itself prints nothing in that case.
run_logged() {
    local log=$1
    shift
    (
        echo "$(date '+%F %T') starting: $*" >> "$log"
        "$@" >> "$log" 2>&1
        code=$?
        sig=""
        if [ "$code" -gt 128 ]; then
            sig=" (SIG$(kill -l $((code - 128)) 2>/dev/null))"
        fi
        # name the script (last argument), not the interpreter
        echo "$(date '+%F %T') $(basename "${!#}") exited with code $code$sig" >> "$log"
    ) &
}

# Unbuffered Python output, so nothing is lost in a buffer if a script dies.
# (Set via the environment rather than "python3 -u" to keep the command lines
# matched by the pkill pattern above unchanged.)
export PYTHONUNBUFFERED=1

# Start Python scripts in the background, logging to /tmp (cleared on reboot)
run_logged /tmp/wearpi-adc.log /home/wearpi/env/bin/python3 /home/wearpi/git/wearpi-py/wearpi-osc-lists-adc-norm-smooth-4in.py
sleep 2
run_logged /tmp/wearpi-controls.log /home/wearpi/env/bin/python3 /home/wearpi/git/wearpi-py/wearpi-osc-lists-controls.py
sleep 2

# Launch Pd patch in nogui mode
FLUCOMA=/usr/lib/puredata/extra/FluidCorpusManipulation
MOSO=/home/wearpi/git/MoSo/abs
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-sound-4in.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-granular.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-granular-cosima-sounds.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-fx.pd &
puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-audioin-rave.pd &

# Keep the OWL-BioSignals-P010 EMG board (BLE-MIDI) routed into Pd's MIDI
# input. The watcher re-connects the two ALSA MIDI ports whenever the board
# drops out and BlueZ reconnects it, or Pd restarts. See midi-watcher.sh for
# details; reconnect history is logged to /tmp/midi-watcher.log.
/home/wearpi/git/wearpi-py/shell/midi-watcher.sh &
