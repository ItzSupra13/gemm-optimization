Commands:
make

sudo cpupower frequency-set -g performance

./run.sh bin/peak

./run.sh bin/ref_openblas_O3 -r 5 | tee results/ref.csv

./run.sh bin/01_naive_O0 -m 1024 -r 3 | tee results/01_O0.csv
./run.sh bin/01_naive_O2 -m 1024 -r 3 | tee results/01_O2.csv
./run.sh bin/01_naive_O3 -m 1024 -r 3 | tee results/01_O3.csv