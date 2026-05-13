import subprocess


def get_lsmod_line(module_name):
    result = subprocess.run(
        ["lsmod"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if line.startswith(module_name + " "):
            return line

    return "Module not found in lsmod output."


def get_proc_modules_line(module_name):
    try:
        with open("/proc/modules", "r") as file:
            for line in file:
                if line.startswith(module_name + " "):
                    return line.strip()
    except FileNotFoundError:
        return "/proc/modules not found."

    return "Module not found in /proc/modules."


def get_modinfo(module_name):
    result = subprocess.run(
        ["modinfo", module_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return "modinfo not available. This can happen for manually inserted local modules."

    return result.stdout


def collect_module_evidence(module_name):
    return {
        "module": module_name,
        "lsmod": get_lsmod_line(module_name),
        "proc_modules": get_proc_modules_line(module_name),
        "modinfo": get_modinfo(module_name)
    }
