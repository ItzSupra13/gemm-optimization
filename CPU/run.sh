#!/usr/bin/env bash
# Run any binary single-threaded, pinned to one P-core hardware thread.
#
#   ./run.sh bin/peak
#   ./run.sh bin/ref_openblas_O3 > results/ref.csv
#   ./run.sh bin/01_naive_O3 -n 64,128,256,512,1024 -r 5 > results/01_O3.csv
#
# CPU=3 ./run.sh ...   to pick another logical CPU (default 2).
#
# On this machine (i7-1355U): logical CPUs 0-3 are the two P-cores (0,1 = core 0;
# 2,3 = core 1), CPUs 4-11 are E-cores. We default to CPU 2 because CPU 0 tends to
# service interrupts, and we leave its SMT sibling (CPU 3) idle so we own the core.

set -euo pipefail

CPU=${CPU:-2}
base=/sys/devices/system/cpu/cpu$CPU/cpufreq
gov=$(cat "$base/scaling_governor" 2>/dev/null || echo unknown)
epp=$(cat "$base/energy_performance_preference" 2>/dev/null || echo unknown)

echo "# pin=cpu$CPU governor=$gov epp=$epp" >&2

if [[ $gov != performance ]]; then
    echo "# WARNING: governor is '$gov'. For stable numbers run:" >&2
    echo "#   sudo cpupower frequency-set -g performance" >&2
fi

if upower -e >/dev/null 2>&1 && ! cat /sys/class/power_supply/AC*/online 2>/dev/null | grep -q 1; then
    echo "# WARNING: laptop looks like it is on battery. Plug in." >&2
fi

# One thread everywhere: the single-thread ladder must not be helped by BLAS threading.
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1

exec taskset -c "$CPU" "$@"