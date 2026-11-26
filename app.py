import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from simulation import run_simulation
from sf_comparison import compare_spreading_factors

ORDER = [f"SF{s}" for s in range(7, 13)]

st.set_page_config(
    page_title="LoRaWAN Scalability Simulator",
    page_icon="📡",
    layout="wide"
)

st.title("📡 LoRaWAN Scalability Simulator")
st.write(
    "Preliminary Prototype — Scalability Limits of LoRaWAN "
    "under Dense Node Deployment"
)

st.info(
    "Simplified single-gateway collision model. "
    "One packet per device, one shared channel, "
    "no capture effect, propagation loss or "
    "inter-SF interference."
)

st.sidebar.header("Simulation Parameters")

num_nodes = st.sidebar.slider(
    "Number of End Devices",
    50, 1000, 200, 50
)

duration = st.sidebar.slider(
    "Simulation Duration (seconds)",
    100, 2000, 1000, 100
)

sf = st.sidebar.selectbox(
    "Spreading Factor",
    [7, 8, 9, 10, 11, 12]
)

payload_size = st.sidebar.slider(
    "Payload Size (bytes)",
    10, 100, 20, 10
)

tab1, tab2 = st.tabs([
    "Single SF Simulation",
    "SF Comparison"
])

with tab1:
    st.header("Single Spreading Factor Simulation")

    if st.button("Run Simulation", type="primary"):
        result = run_simulation(
            num_nodes=num_nodes,
            duration=duration,
            sf=sf,
            payload_size=payload_size
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Devices", result["nodes"])
        c2.metric("PDR", f'{result["pdr"]}%')
        c3.metric("Collision Rate", f'{result["collision_rate"]}%')
        c4.metric("Time on Air", f'{result["airtime_ms"]} ms')

        node_counts = [50, 100, 200, 500, 1000]

        df = pd.DataFrame([
            run_simulation(
                num_nodes=n,
                duration=duration,
                sf=sf,
                payload_size=payload_size
            )
            for n in node_counts
        ])

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(df["nodes"], df["pdr"], marker="o", label="PDR")
        ax.plot(
            df["nodes"], df["collision_rate"],
            marker="s", label="Collision Rate"
        )
        ax.set_xlabel("Number of End Devices")
        ax.set_ylabel("Percentage (%)")
        ax.set_ylim(0, 100)
        ax.set_title(f"Scalability Analysis — SF{sf}")
        ax.grid(True)
        ax.legend()

        st.pyplot(fig)
        plt.close(fig)

        st.dataframe(df, use_container_width=True)

        st.download_button(
            "Download Single SF Results",
            df.to_csv(index=False),
            file_name="single_sf_results.csv",
            mime="text/csv"
        )

with tab2:
    st.header("Spreading Factor Comparison")

    st.write(
        "Compare SF7–SF12 across different network "
        "densities using repeated simulation runs."
    )

    repetitions = st.slider(
        "Number of Simulation Runs",
        1, 50, 10
    )

    if st.button("Compare All SFs", type="primary"):

        with st.spinner("Running simulations..."):
            summary_df, runs_df = compare_spreading_factors(
                duration=duration,
                payload_size=payload_size,
                repetitions=repetitions
            )

        st.subheader("PDR Comparison")
        pdr_table = summary_df.pivot(
            index="Nodes", columns="SF", values="PDR (%)"
        )[ORDER]
        st.line_chart(pdr_table)

        st.subheader("Collision Rate Comparison")
        collision_table = summary_df.pivot(
            index="Nodes", columns="SF", values="Collision Rate (%)"
        )[ORDER]
        st.line_chart(collision_table)

        st.subheader("Time on Air Comparison")
        airtime = (
            summary_df.drop_duplicates(subset=["SF"])
            .set_index("SF")["Time on Air (ms)"]
            .reindex(ORDER)
        )
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(airtime.index, airtime.values)
        ax.set_ylim(bottom=0)
        ax.set_ylabel("Time on Air (ms)")
        ax.set_title("Time on Air by Spreading Factor")
        st.pyplot(fig)
        plt.close(fig)

        st.subheader("Comparison Results")
        st.dataframe(summary_df, use_container_width=True)

        st.download_button(
            "Download SF Comparison CSV",
            summary_df.to_csv(index=False),
            file_name="sf_comparison_results.csv",
            mime="text/csv"
        )

        st.download_button(
            "Download Per-run Results",
            runs_df.to_csv(index=False),
            file_name="sf_comparison_per_run.csv",
            mime="text/csv"
        )