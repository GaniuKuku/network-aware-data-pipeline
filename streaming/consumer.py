import argparse
import json

from confluent_kafka import Consumer


TOPIC = "network-telemetry"


def create_consumer(group_id: str) -> Consumer:
    """Create and configure the Kafka consumer."""
    return Consumer(
        {
            "bootstrap.servers": "localhost:19092",
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        }
    )


def main():
    parser = argparse.ArgumentParser(
        description="Consume network telemetry from Redpanda."
    )

    parser.add_argument(
        "--group",
        type=str,
        default="network-telemetry-consumer",
        help="Kafka consumer group ID.",
    )

    parser.add_argument(
        "--events",
        type=int,
        default=5,
        help="Number of events to consume.",
    )

    parser.add_argument(
    "--experiment",
    type=str,
    default=None,
    help="Only consume events belonging to this experiment.",
    )

    args = parser.parse_args()

    consumer = create_consumer(args.group)

    consumer.subscribe([TOPIC])

    consumed = 0

    try:
        while consumed < args.events:
            message = consumer.poll(1.0)

            if message is None:
                continue

            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

            event = json.loads(message.value().decode("utf-8"))

            if args.experiment and event["experiment_id"] != args.experiment:
                continue

            print(
                f"Consumed sequence={event['sequence_number']} "
                f"experiment={event['experiment_id']} "
                f"partition={message.partition()} "
                f"offset={message.offset()}"
            )

            consumed += 1

    finally:
        consumer.close()


if __name__ == "__main__":
    main()
