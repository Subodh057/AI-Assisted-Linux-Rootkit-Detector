import os
import subprocess


BASELINE_PATH = "data/baseline_modules.txt"


def get_loaded_modules():
    result = subprocess.run(
        ["lsmod"],
        capture_output=True,
        text=True
    )

    modules = set()
    lines = result.stdout.strip().split("\n")[1:]

    for line in lines:
        parts = line.split()
        if parts:
            modules.add(parts[0])

    return modules


def save_module_baseline():
    os.makedirs("data", exist_ok=True)

    modules = get_loaded_modules()

    with open(BASELINE_PATH, "w") as file:
        for module in sorted(modules):
            file.write(module + "\n")

    print(f"Baseline saved with {len(modules)} modules.")


def load_baseline_modules():
    if not os.path.exists(BASELINE_PATH):
        return None

    with open(BASELINE_PATH, "r") as file:
        return set(line.strip() for line in file if line.strip())


def check_module_changes():
    findings = []

    baseline_modules = load_baseline_modules()
    current_modules = get_loaded_modules()

    if baseline_modules is None:
        findings.append({
            "type": "Baseline Missing",
            "risk": "Info",
            "reason": "No module baseline found. Run: python main.py --baseline"
        })
        return findings

    new_modules = current_modules - baseline_modules
    removed_modules = baseline_modules - current_modules

    for module in sorted(new_modules):
        findings.append({
            "type": "New Kernel Module",
            "name": module,
            "risk": "Medium",
            "reason": "Module was not present in the clean baseline"
        })

    for module in sorted(removed_modules):
        findings.append({
            "type": "Removed Kernel Module",
            "name": module,
            "risk": "Low",
            "reason": "Module existed in baseline but is not currently loaded"
        })

    return findings
