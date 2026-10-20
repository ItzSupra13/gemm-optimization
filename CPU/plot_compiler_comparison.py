import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# Configuration
# --------------------------------------------------

RESULTS = Path("results")
PEAK_GFLOPS = 159.1  # Measured peak from your FMA benchmark

FILES = {
    "IKJ O0": RESULTS / "02_ikj_O0.csv",
    "IKJ O1": RESULTS / "02_ikj_O1.csv",
    "IKJ O2": RESULTS / "02_ikj_O2.csv",
    "IKJ O3": RESULTS / "02_ikj_O3.csv",
}

# --------------------------------------------------
# Load the benchmark CSV files
# Lines beginning with # are metadata, not CSV rows.
# --------------------------------------------------
sizes = [64, 128, 256, 512, 1024, 2048]
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
# Plot 2: IKJ kernel compiler comparison (Mix of Fast and Intuitive)
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(11, 6))

for name in ["IKJ O0", "IKJ O1", "IKJ O2", "IKJ O3"]:
    if name not in data:
        continue

    df = data[name]

    ax.plot(
        df["n"],
        df["median_gflops"],
        marker="o",
        linewidth=2,
        markersize=5,
        label=name,
    )

ax.set_title("IKJ: Effect of Compiler Optimization")
ax.set_xlabel("Matrix dimension n (n × n)")
ax.set_xticks(sizes)
ax.set_xticklabels([str(n) for n in sizes])

ax.set_ylabel("Median throughput (GFLOPS)")
ax.grid(True, alpha=0.3)
ax.legend()
fig.tight_layout()
fig.savefig("plots/ikj_compiler_comparison.png", dpi=200)
plt.show()

print("Saved ikj_compiler_comparison.png")
