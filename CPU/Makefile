.RECIPEPREFIX := >
CC      ?= gcc
WARN    := -std=gnu11 -Wall -Wextra
LIBS    := -lopenblas -lm

KERNELS := 01_naive 02_ikj

BINS := bin/ref_openblas_03 bin/peak \
        $(foreach k,$(KERNELS),bin/$(k)_O0 bin/$(k)_O2 bin/$(k)_O3)

.PHONY: all clean
all: $(BINS)

bin:
> mkdir -p bin

bin/%_O0: %.c bench.c bench.h util.h | bin
> $(CC) $(WARN) -O0 -DBUILD_TAG='"-O0"' $< bench.c -o $@ $(LIBS)

bin/%_O2: %.c bench.c bench.h util.h | bin
> $(CC) $(WARN) -O2 -DBUILD_TAG='"-O2"' $< bench.c -o $@ $(LIBS)

bin/%_O3: %.c bench.c bench.h util.h | bin
> $(CC) $(WARN) -O3 -march=native -ffast-math \
>   -DBUILD_TAG='"-O3 -march=native -ffast-math"' $< bench.c -o $@ $(LIBS)

bin/peak: peak.c util.h | bin
> $(CC) $(WARN) -O3 -march=native peak.c -o $@

clean:
> rm -rf bin
