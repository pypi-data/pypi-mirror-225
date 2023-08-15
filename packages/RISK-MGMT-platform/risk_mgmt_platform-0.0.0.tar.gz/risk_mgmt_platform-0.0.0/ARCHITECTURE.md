# Architecture

This project is pre-release and this may change quite a bit.

## Goal

The goal of this project is to be an engine for options trading.

For that it will need to automate:

- Data Collection
- Data Analysis
- Trading

## Repo Structure

At least initially this will be a single project, but the components will be
split into their own clearly separated modules under src.

## Components

This section goes into a little more detail about the components that make up
the platform.

### Collection

Data collectors will exist to gather the information needed for analysis.

Their responsibilities are to collect and store the information in a normalized
way so that the analyzers can process the data.

### Analysis

Analyzers will observe changes in the collected data and generate facts,
statistics and predictions about the data.

### Trading

The automated traders will take information from the analyzers to actually make
trades.

### Tests

We'll want a strong foundation of tests to minimize costly mistakes in the
code. See [CONTRIBUTING.md](./CONTRIBUTING.md) for more info about testing.
