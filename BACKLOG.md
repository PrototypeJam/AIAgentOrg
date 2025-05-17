# Backlog

This file tracks outstanding tasks and feature ideas for the project. Items are recorded here so contributors can coordinate on upcoming work.

## Items

1. **Document module3 differences**
   - Write a comprehensive explanation comparing `module3.py` and `module3-gem.py`.
   - Outline additional fields such as `rating` and `improvement_suggestions` introduced in `module3-gem.py`.
   - Highlight the modified logging setup in `module3-gem.py` with its verbose logger compared to the single logger used in `module3.py`.
   - Note that downstream modules may require updates to consume these new fields.

2. **Add uniform logging and tracing for all modules**
   - Extract the advanced logging and OpenTelemetry setup from `module1-opentelemetry-gm-1156.py` into reusable utilities (e.g., `tracing_utils.py`).
   - Include functions like `setup_logging`, `setup_opentelemetry`, `capture_step`, `traced_span`, and the `DetailedLoggingHooks` class.
   - Import these utilities in `module2.py` through `module6.py` so each module writes logs to the `logs` directory and stores traces in `manual_traces.json` and timestamped OpenTelemetry files.
   - Wrap the major steps of each module in `traced_span` contexts and use `DetailedLoggingHooks` for all agents to record start/end events, tool calls, and outputs.
   - Propagate a shared `process_id` or `trace_id` between modules to link traces across the full workflow.
   - Document the new setup and usage in the README, including instructions for viewing trace files.
