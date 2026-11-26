# LoRaWAN Scalability Simulator (preliminary prototype)

Single-gateway LoRaWAN uplink simulation for the Honours project
"Scalability Limits of LoRaWAN under Dense Node Deployment".

This is a preliminary prototype. It implements fixed spreading factors
SF7–SF12, one packet per device and a binary overlap collision rule.
Capture effect, inter-SF interference, propagation loss, spatial
distributions, ADR and energy estimation are planned and not implemented.

## Requirements

Python 3.13 (tested with 3.13.18). Packages are pinned in `requirements.txt`.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the interface

```bash
streamlit run app.py
```

Open http://localhost:8501. The "SF Comparison" tab runs repeated simulations
with seeds 42 to 51 and provides two CSV downloads: the summary and the per-run results.

## Files

- `simulation.py`: airtime calculation and the binary collision model
- `sf_comparison.py`: repeated runs over SF7–SF12 and device counts
- `app.py`: Streamlit interface
- `requirements.txt`: pinned package versions

## Reproducibility

The results in the Honours report were produced at commit
`9e9d1a386ac3e7e18e970a8108b331df40653b69`.