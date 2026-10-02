# Queue Backups and Experiments

This directory is the unified home for historical queue snapshots and isolated queue experiments.

## Contents

- Timestamped `queue*.jsonl` files are point-in-time snapshots created before queue migrations, repairs, resets, or bulk seeding.
- `tmp/` contains abandoned or one-off queue experiments retained for audit and recovery.
- `twelve-sentence-queue/` contains the isolated twelve-sentence experiment queue.

## Live Queue Boundary

The live research runner does not read this directory by default. Its source of truth remains:

- `../../queue.jsonl`
- `../../queue.done.jsonl`
- `../../queue.control.json`

Do not edit historical snapshots in place. Before a bulk queue change, copy both live JSONL files here using a timestamped, purpose-specific filename.
