# AetherMind

AetherMind is an experimental cognitive architecture intended to explore long term memory and autonomous reasoning. The code base provides a modular brain consisting of several memory tiers, a simple BDI style goal manager and a reasoning loop with safety guards. It is **not** a full autonomous agent but a research playground.

## Components
- `Brain` & `MemoryController` – manage short term, episodic, semantic, procedural and archival memories.
- `GoalManager` – tracks goals and beliefs using a priority queue.
- `ReasoningLoop` – perception/interpretation/evaluation cycle that consults the goal manager.
- `Identity` – loads and stores the agent identity from `identity.yaml` and allows reflection logging.
- `cli` – small interactive interface to experiment with the brain.

The project intentionally prevents self modification through `SelfModificationGuard` and includes an `EmergencyShutdown` phrase for quick termination.

Run the CLI with:
```bash
python -m aethermind
```
