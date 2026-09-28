# Telemetry Data Schema

## Purpose

This schema defines the events produced by the synthetic telemetry generator.

The network-related fields are inspired by the characteristics of real network flow data such as CIC-IDS2017. Additional fields are included to support the data pipeline experiments.

CIC-IDS2017 is used as a reference for realistic network behaviour. It is not the runtime dataset for the pipeline.

## Event Schema

| Field                   | Type     | Description                                                      |
| ----------------------- | -------- | ---------------------------------------------------------------- |
| `event_id`              | string   | Unique identifier for the telemetry event                        |
| `event_timestamp`       | datetime | Time the event was generated                                     |
| `sequence_number`       | integer  | Ordered event number used to detect missing or duplicated events |
| `source_service`        | string   | Service generating the event                                     |
| `destination_service`   | string   | Service receiving the event                                      |
| `source_ip`             | string   | Source IP address                                                |
| `destination_ip`        | string   | Destination IP address                                           |
| `source_port`           | integer  | Source network port                                              |
| `destination_port`      | integer  | Destination network port                                         |
| `protocol`              | string   | Network protocol such as TCP or UDP                              |
| `flow_duration_ms`      | integer  | Duration of the network flow in milliseconds                     |
| `forward_packet_count`  | integer  | Number of packets sent from source to destination                |
| `backward_packet_count` | integer  | Number of packets sent from destination to source                |
| `bytes_sent`            | integer  | Bytes sent from source to destination                            |
| `bytes_received`        | integer  | Bytes received from destination                                  |
| `flow_bytes_per_sec`    | float    | Approximate bytes transferred per second                         |
| `flow_packets_per_sec`  | float    | Approximate packets transferred per second                       |
| `response_time_ms`      | integer  | Application response time                                        |
| `status`                | string   | Event outcome such as `success`, `timeout`, or `error`           |
| `experiment_id`         | string   | Identifier for the network experiment                            |

## Why These Fields Matter

### Network behaviour

These fields allow us to model network traffic characteristics:

* `source_ip`
* `destination_ip`
* `source_port`
* `destination_port`
* `protocol`
* `flow_duration_ms`
* `forward_packet_count`
* `backward_packet_count`
* `bytes_sent`
* `bytes_received`
* `flow_bytes_per_sec`
* `flow_packets_per_sec`

These characteristics are relevant because CIC-IDS2017 contains flow duration, forward and backward packet counts, forward and backward byte counts, and traffic-rate features among its network-flow measurements.

Separating forward and backward packet counts also gives the generator better control over the direction of network traffic.


### Data pipeline reliability

These fields are specifically useful for our engineering experiments:

* `event_id` allows us to identify individual records.
* `sequence_number` allows us to detect missing, duplicated or reordered events.
* `experiment_id` allows us to compare different network conditions.
* `status` allows us to distinguish successful events from failures and timeouts.

### Application behaviour

`response_time_ms` gives us an application-level measurement that can be compared with the network conditions applied during an experiment.

## What We Are Not Including

We are deliberately not including attack labels or machine-learning features as part of the runtime telemetry schema.

The project is not an intrusion detection system.

The purpose of the telemetry is to measure how network conditions affect:

* Data ingestion
* Throughput
* Latency
* Consumer lag
* Failures
* Recovery
* Data integrity

## Data Flow

```text
CIC-IDS2017
     │
     │ study realistic network-flow characteristics
     ▼
Telemetry Schema
     │
     ▼
Synthetic Telemetry Generator
     │
     ▼
Network Laboratory
     │
     ├── latency
     ├── bandwidth limits
     ├── packet loss
     └── network outages
     │
     ▼
Streaming Pipeline
     │
     ▼
Storage and Transformation
     │
     ▼
Pipeline Measurements
```

## Design Principle

The synthetic generator gives us control over event rate, message characteristics, experiment duration and repeatability.

This allows the same workload to be tested under different network conditions so that changes in pipeline behaviour can be measured.
