Commands:
make clean
make

sudo cpupower frequency-set -g performance

./run.sh bin/peak

./run.sh bin/ref_openblas -r 5 | tee results/ref.csv

./run.sh bin/01_naive -r 3 | tee results/01.csv

./run.sh bin/02_ikj -r 3 | tee results/02.csv

For Compliler comparison:
./run.sh bin/02_ikj_O0 -m 2048 -r 3 | tee results/02_ikj_O0.csv
./run.sh bin/02_ikj_O1 -m 2048 -r 3 | tee results/02_ikj_O1.csv
./run.sh bin/02_ikj_O2 -m 2048 -r 3 | tee results/02_ikj_O2.csv
./run.sh bin/02_ikj_O3 -m 2048 -r 3 | tee results/02_ikj_O3.csv


For uv plot files running install:
pandas matplotlib

To Do in blog:
- Add idea of gcc flags and we use 03 throughout + Show comparison with img
