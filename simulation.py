import random


def calculate_airtime(sf, payload_size=20, bandwidth=125000):
    """
    Approximate LoRa packet Time on Air (seconds).
    Assumptions:
    - Coding rate 4/5
    - Explicit header
    - CRC enabled
    - 8-symbol preamble
    """

    if sf not in range(7, 13):
        raise ValueError("Spreading Factor must be SF7-SF12")

    if payload_size < 0:
        raise ValueError("Payload size cannot be negative")

    symbol_time = (2 ** sf) / bandwidth

    # Low Data Rate Optimization for BW125
    de = 1 if sf >= 11 and bandwidth == 125000 else 0

    numerator = (
        8 * payload_size - 4 * sf + 28 + 16
    )

    denominator = 4 * (sf - 2 * de)

    payload_symbols = 8 + max(
        0,
        ((numerator + denominator - 1) // denominator) * 5
    )

    preamble_time = (8 + 4.25) * symbol_time
    payload_time = payload_symbols * symbol_time

    return preamble_time + payload_time


def run_simulation(
    num_nodes,
    duration=1000,
    sf=7,
    payload_size=20,
    seed=42
):
    """
    Simplified single-gateway LoRaWAN simulation.
    Each device sends one packet.
    Overlapping packets collide.
    """

    random.seed(seed)

    airtime = calculate_airtime(sf, payload_size)

    if duration <= airtime:
        raise ValueError(
            "Simulation duration must exceed packet airtime"
        )

    transmissions = []

    for node in range(num_nodes):
        start = random.uniform(0, duration - airtime)
        end = start + airtime
        transmissions.append((start, end, node))

    transmissions.sort()

    collided = set()

    for i in range(len(transmissions)):
        start_i, end_i, node_i = transmissions[i]

        for j in range(i + 1, len(transmissions)):
            start_j, end_j, node_j = transmissions[j]

            if start_j >= end_i:
                break

            if start_i < end_j and start_j < end_i:
                collided.add(node_i)
                collided.add(node_j)

    delivered = num_nodes - len(collided)

    pdr = delivered / num_nodes * 100
    collision_rate = len(collided) / num_nodes * 100

    return {
        "nodes": num_nodes,
        "sf": sf,
        "payload_size": payload_size,
        "airtime_ms": round(airtime * 1000, 2),
        "delivered": delivered,
        "collided": len(collided),
        "pdr": round(pdr, 2),
        "collision_rate": round(collision_rate, 2)
    }


if __name__ == "__main__":
    for sf in range(7, 13):
        result = run_simulation(
            num_nodes=500,
            sf=sf,
            payload_size=20
        )
        print(result)