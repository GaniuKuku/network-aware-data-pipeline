import argparse
import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

def generate_event(sequence_number: int, experiment_id: str) -> dict:
    """Generate one synthetic network telemetry event."""
    flow_duration_ms = random.randint(1, 5000)
    forward_packet_count = random.randint(1, 100)
    backward_packet_count = random.randint(0, 100)

    bytes_sent = random.randint(40, 50000)
    bytes_received = random.randint(0, 100000)

    total_bytes = bytes_sent + bytes_received
    total_packets = forward_packet_count + backward_packet_count

    flow_bytes_per_sec = round(
        total_bytes / (flow_duration_ms / 1000),
        2,
    )

    flow_packets_per_sec = round(
        total_packets / (flow_duration_ms / 1000),
        2,
    )

    return {
        "event_id": str(uuid.uuid4()),
        "event_timestamp": datetime.now(timezone.utc).isoformat(),
        "sequence_number": sequence_number,
        "source_service": "telemetry-producer",
        "destination_service": "telemetry-consumer",
        "source_ip": "10.10.0.1",
        "destination_ip": "10.10.0.2",
        "source_port": random.randint(1024, 65535),
        "destination_port": 9092,
        "protocol": random.choice(["TCP", "UDP"]),
        "flow_duration_ms": flow_duration_ms,
        "forward_packet_count": forward_packet_count,
        "backward_packet_count": backward_packet_count,
        "bytes_sent": bytes_sent,
        "bytes_received": bytes_received,
        "flow_bytes_per_sec": flow_bytes_per_sec,
        "flow_packets_per_sec": flow_packets_per_sec,
        "response_time_ms": random.randint(1, 1000),
        "status": random.choice(["success", "success", "success", "timeout", "error"]),
        "experiment_id": experiment_id,
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate synthetic network telemetry events."
    )

    parser.add_argument(
        "--events",
        type=int,
        default=1,
        help="Number of events to generate.",
    )

    parser.add_argument(
        "--rate",
        type=float,
        default=1.0,
        help="Target number of events to generate per second.",
    )

    parser.add_argument(
        "--experiment",
        type=str,
        default="baseline-001",
        help="Experiment identifier.",
    )

    # Added the missing --output argument
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Path to save the output as a JSONL file. Prints to stdout if not specified.",
    )

    args = parser.parse_args()

    interval = 1.0 / args.rate

    # Open file context if an output file path is provided
    if args.output:
        dir_name = os.path.dirname(args.output)

        if dir_name:
            os.makedirs(dir_name, exist_ok=True)

        with open(args.output, "w", encoding="utf-8") as out_file:
            for sequence_number in range(1, args.events + 1):
                event = generate_event(
                    sequence_number=sequence_number,
                    experiment_id=args.experiment,
                )

                json_line = json.dumps(event)
                out_file.write(json_line + "\n")
                out_file.flush()

                if sequence_number < args.events:
                    time.sleep(interval)

    else:
        for sequence_number in range(1, args.events + 1):
            event = generate_event(
                sequence_number=sequence_number,
                experiment_id=args.experiment,
            )

            print(json.dumps(event))

            if sequence_number < args.events:
                time.sleep(interval)
