import pandas as pd
from simulation import run_simulation


def compare_spreading_factors(
    node_counts=None,
    duration=1000,
    payload_size=20,
    repetitions=10
):
    """
    Compare SF7-SF12 using repeated simulation runs.
    Each run uses a different random seed.
    """
    if node_counts is None:
        node_counts = [50, 100, 200, 500, 1000]

    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1")

    results = []

    for sf in range(7, 13):
        for nodes in node_counts:
            runs = []

            for repeat in range(repetitions):
                result = run_simulation(
                    num_nodes=nodes,
                    duration=duration,
                    sf=sf,
                    payload_size=payload_size,
                    seed=42 + repeat
                )
                runs.append(result)

            results.append({
                "SF": f"SF{sf}",
                "Nodes": nodes,
                "PDR (%)": round(
                    sum(r["pdr"] for r in runs) / repetitions,
                    2
                ),
                "Collision Rate (%)": round(
                    sum(r["collision_rate"] for r in runs)
                    / repetitions,
                    2
                ),
                "Time on Air (ms)": runs[0]["airtime_ms"]
            })

    return pd.DataFrame(results)


if __name__ == "__main__":
    df = compare_spreading_factors()
    print(df.to_string(index=False))