import argparse
import json
import sys

from confluent_kafka import Producer

from producer.generator import generate_event


TOPIC = "network-telemetry"


def delivery_report(err, msg):
    """Report the result of a Kafka message delivery."""
    if err is not None:
        print(
            f"Delivery failed: {err}",
            file=sys.stderr,
        )
        return

    print(
        f"Delivered sequence={msg.key().decode('utf-8')} "
        f"partition={msg.partition()} "
        f"offset={msg.offset()}"
    )


def create_producer() -> Producer:
    """Create and configure the Kafka producer."""
    return Producer(
        {
            "bootstrap.servers": "localhost:19092",
        }
    )


def publish_event(producer: Producer, event: dict):
    """Publish one telemetry event to Redpanda."""
    producer.produce(
        TOPIC,
        key=str(event["sequence_number"]),
        value=json.dumps(event),
        callback=delivery_report,
    )

    producer.poll(0)


def stream_generated_events(
    producer: Producer,
    events: int,
    experiment: str,
):
    """Generate and publish telemetry events."""
    for sequence_number in range(1, events + 1):
        event = generate_event(
            sequence_number=sequence_number,
            experiment_id=experiment,
        )

        publish_event(producer, event)

def validate_event(event: dict, line_number: int):
    """Validate the fields required for streaming."""
    required_fields = [
        "event_id",
        "event_timestamp",
        "sequence_number",
        "experiment_id",
    ]

    missing_fields = [
        field for field in required_fields
        if field not in event
    ]

    if missing_fields:
        raise ValueError(
            f"Line {line_number} is missing required fields: "
            f"{', '.join(missing_fields)}"
        )

def stream_jsonl(
    producer: Producer,
    input_file: str,
):
    """Read and publish telemetry events from a JSONL workload."""
    with open(input_file, "r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                event = json.loads(line)
                validate_event(event, line_number)
            except json.JSONDecodeError as error:
                print(
                    f"Invalid JSON on line {line_number}: {error}",
                    file=sys.stderr,
                )
                continue

            publish_event(producer, event)


def main():
    parser = argparse.ArgumentParser(
        description="Stream synthetic network telemetry to Redpanda."
    )

    parser.add_argument(
        "--events",
        type=int,
        default=10,
        help="Number of telemetry events to generate.",
    )

    parser.add_argument(
        "--experiment",
        type=str,
        default="streaming-001",
        help="Experiment identifier for generated events.",
    )

    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to a JSONL workload to replay.",
    )

    args = parser.parse_args()

    producer = create_producer()

    if args.input:
        stream_jsonl(
            producer=producer,
            input_file=args.input,
        )
    else:
        stream_generated_events(
            producer=producer,
            events=args.events,
            experiment=args.experiment,
        )

    producer.flush()


if __name__ == "__main__":
    main()
