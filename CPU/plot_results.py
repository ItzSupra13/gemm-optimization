import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Configuration
# --------------------------------------------------

RESULTS = Path("results")
PEAK_GFLOPS = 159.1  # Measured peak from your FMA benchmark

FILES = {
    "OpenBLAS": RESULTS / "ref.csv",
    "IKJ": RESULTS / "02.csv",
    "Naive": RESULTS / "01.csv",
}

# --------------------------------------------------
# Load the benchmark CSV files
# Lines beginning with # are metadata, not CSV rows.
# --------------------------------------------------
sizes = [64, 128, 256, 512, 1024, 2048, 4096, 8192]
positions = range(len(sizes))
data = {}

for name, path in FILES.items():
    if not path.exists():
        print(f"Skipping {name}: {path} not found")
        continue

    df = pd.read_csv(path, comment="#")

    # Keep only successful correctness checks.
    df = df[df["ok"] == 1].copy()

    df["n"] = pd.to_numeric(df["n"])
    df["median_gflops"] = pd.to_numeric(df["median_gflops"])

    # Sort matrix sizes so lines connect in the right order.
    df = df.sort_values("n")

    data[name] = df

# --------------------------------------------------
# Plot 1: Full performance ladder
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))

for name, df in data.items():
    ax.plot(
        df["n"],
        df["median_gflops"],
        marker="o",
        linewidth=2,
        label=name,
    )

ax.axhline(
    PEAK_GFLOPS,
    linestyle="--",
    linewidth=1.8,
    label=f"Measured FMA peak ({PEAK_GFLOPS:.1f} GFLOPS)",
)

ax.set_title("CPU Matrix Multiplication: Performance Ladder")
ax.set_xlabel("Matrix dimension n (n × n)")
ax.set_ylabel("Median throughput (GFLOPS)")

ax.set_xscale("log", base=2) # comment this out to see the real scale in x-axis
ax.set_xticks(sizes)
ax.set_xticklabels([str(n) for n in sizes])

ax.set_yscale("log")
ax.grid(True, which="both", alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("plots/performance_ladder.png", dpi=200)
plt.show()