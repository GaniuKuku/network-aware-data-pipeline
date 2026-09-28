# Dataset Strategy

## Primary Dataset

CIC-IDS2017 is used as a real-world reference dataset for this project.

## Why We Use It

The project needs a realistic network traffic workload.

Instead of generating completely random telemetry, CIC-IDS2017 gives us real network traffic characteristics that we can study and use to design our synthetic telemetry generator.

## How We Use It

CIC-IDS2017 is used for:

- Understanding network flow characteristics
- Understanding traffic volume and packet behaviour
- Identifying useful telemetry fields
- Calibrating our synthetic data generator

## What We Are Not Building

This is not an intrusion detection project.

We are not building a machine learning model to detect attacks.

The main objective is to study how network conditions affect a data pipeline.

## Synthetic Telemetry

Our own telemetry generator will produce the actual workload used in the experiments.

This gives us control over:

- Event generation rate
- Message size
- Number of events
- Flow characteristics
- Experiment duration
- Repeatability

## Project Flow

CIC-IDS2017
    ↓
Study network characteristics
    ↓
Design telemetry schema
    ↓
Synthetic telemetry generator
    ↓
Network
    ↓
Streaming pipeline
    ↓
Processing and storage
    ↓
Measure pipeline behaviour

## Why This Approach

Using real data as a reference gives the workload more realistic characteristics.

Using synthetic data for the actual experiments gives us control and makes experiments repeatable.
