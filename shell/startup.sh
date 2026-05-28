#!/bin/bash

# Kill any stale instances before launching
pkill -f "wearpi-osc-lists" 2>/dev/null
pkill -f puredata 2>/dev/null
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
puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-granular-cosima-sounds.pd &
# puredata -nogui -stderr -audiodev "4" -path "$FLUCOMA" -path "$MOSO" -lib fluid_libmanipulation /home/wearpi/git/wearpi-py/pd/wearpi-regression-fx.pd &