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

# Start Python scripts in the background

/home/wearpi/env/bin/python3 /home/wearpi/git/wearpi-py/wearpi-osc-lists-adc-norm-smooth-4in.py &
sleep 2
/home/wearpi/env/bin/python3 /home/wearpi/git/wearpi-py/wearpi-osc-lists-controls.py &
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
