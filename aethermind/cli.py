from __future__ import annotations
import argparse
from .brain import Brain
from .goals import GoalManager
from .reasoning import ReasoningLoop
from .safeguard import SelfModificationGuard, EmergencyShutdown
from .identity import Identity


def main() -> None:
    parser = argparse.ArgumentParser(description="Interact with AetherMind")
    parser.add_argument("--identity", default="identity.yaml")
    args = parser.parse_args()

    identity = Identity.load(args.identity)
    brain = Brain()
    goals = GoalManager()
    guard = SelfModificationGuard()
    shutdown = EmergencyShutdown()
    loop = ReasoningLoop(brain, goals, guard=guard, shutdown=shutdown)

    print(f"Hello, I am {identity.name}. {identity.purpose}")
    print("Type 'recall' to view recent memories or 'quit' to exit.")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"quit", "exit"}:
                break
            if user_input.lower() == "recall":
                events = brain.recall()
                print("Recent memories:")
                for e in events:
                    if hasattr(e, "data"):
                        print("-", e.data)
                    else:
                        print("-", e)
                continue
            loop.cycle(user_input)
        except KeyboardInterrupt:
            print("\nStopped")
            break
        except SystemExit as e:
            print(e)
            break
        except Exception as exc:
            print("Error:", exc)


if __name__ == "__main__":
    main()
