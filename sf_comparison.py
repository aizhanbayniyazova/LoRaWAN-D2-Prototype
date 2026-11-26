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
    Each run uses a different random seed (42 to 42 + repetitions - 1).
    Returns the summary table and the per-run table.
    """
    if node_counts is None:
        node_counts = [50, 100, 200, 500, 1000]

    if repetitions < 1:
        raise ValueError("Repetitions must be at least 1")

    summary = []
    run_records = []

    for sf in range(7, 13):
        for nodes in node_counts:
            runs = []

            for repeat in range(repetitions):
                seed = 42 + repeat
                result = run_simulation(
                    num_nodes=nodes,
                    duration=duration,
                    sf=sf,
                    payload_size=payload_size,
                    seed=seed
                )
                runs.append(result)
                run_records.append({
                    "SF": f"SF{sf}",
                    "Nodes": nodes,
                    "Seed": seed,
                    "PDR (%)": result["pdr"],
                    "Collision Rate (%)": result["collision_rate"],
                    "Time on Air (ms)": result["airtime_ms"],
                })

            summary.append({
                "SF": f"SF{sf}",
                "Nodes": nodes,
                "PDR (%)": round(
                    sum(r["pdr"] for r in runs) / repetitions, 2
                ),
                "Collision Rate (%)": round(
                    sum(r["collision_rate"] for r in runs) / repetitions, 2
                ),
                "Time on Air (ms)": runs[0]["airtime_ms"],
            })

    return pd.DataFrame(summary), pd.DataFrame(run_records)


if __name__ == "__main__":
    summary_df, runs_df = compare_spreading_factors()
    print(summary_df.to_string(index=False))