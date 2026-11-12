import json
import subprocess
import sys
from pathlib import Path

STATE_FILE = Path(".conductor_remediation_state.json")


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"attempts": 0, "last_error": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def run_tests():
    print("Running tests for remediation...")
    result = subprocess.run(
        ["uv", "run", "pytest", "-v", "--cov=src"], capture_output=True, text=True
    )
    return result.returncode, result.stdout, result.stderr


def main():
    state = load_state()
    rc, out, err = run_tests()

    if rc == 0:
        print("SUCCESS: Tests passed. Resetting circuit breaker.")
        save_state({"attempts": 0, "last_error": None})
        sys.exit(0)

    state["attempts"] += 1
    state["last_error"] = err if err else out[-1000:]  # Capture tail of output
    save_state(state)

    if state["attempts"] >= 3:
        print(f"CIRCUIT BREAKER TRIGGERED: Failed {state['attempts']} times.")
        print(f"LAST ERROR: {state['last_error']}")
        sys.exit(1)

    print(f"REMEDIATION REQUIRED: Attempt {state['attempts']}/3. Error captured in state file.")
    sys.exit(2)  # Code 2 means "Retry allowed"


if __name__ == "__main__":
    main()
