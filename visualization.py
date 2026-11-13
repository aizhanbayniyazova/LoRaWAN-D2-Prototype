import matplotlib.pyplot as plt
from simulation import run_simulation

node_counts = [50, 100, 200, 500, 1000]
pdr_values = []
collision_values = []

for nodes in node_counts:
    result = run_simulation(nodes)
    pdr_values.append(result["pdr"])
    collision_values.append(result["collision_rate"])

plt.plot(node_counts, pdr_values, marker="o", label="PDR")
plt.plot(
    node_counts,
    collision_values,
    marker="s",
    label="Collision Rate"
)

plt.xlabel("Number of End Devices")
plt.ylabel("Percentage (%)")
plt.title("LoRaWAN Scalability Simulation")
plt.ylim(0, 100)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()