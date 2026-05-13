import sys
from scanner.ai_analyzer import analyze_module_with_ai
from scanner.module_check import save_module_baseline, check_module_changes
from scanner.module_details import collect_module_evidence


def print_findings(findings):
    print("\nRootWatch AI Scan Result")
    print("=" * 60)

    if not findings:
        print("No suspicious kernel module changes found.")
        return

    for finding in findings:
        print()
        print(f"Type: {finding.get('type')}")
        print(f"Risk: {finding.get('risk')}")
        print(f"Reason: {finding.get('reason')}")

        if "name" in finding:
            module_name = finding.get("name")
            print(f"Name: {module_name}")

            if finding.get("type") == "New Kernel Module":
                evidence = collect_module_evidence(module_name)

                print("\nEvidence")
                print("-" * 30)

                print("lsmod:")
                print(evidence["lsmod"])

                print("\n/proc/modules:")
                print(evidence["proc_modules"])

                print("\nmodinfo:")
                print(evidence["modinfo"])
                print("\nAI Analysis")
                print("-" * 30)
                ai_result = analyze_module_with_ai(evidence)
                print(ai_result)
def run_scan():
    findings = []
    findings.extend(check_module_changes())
    print_findings(findings)


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--baseline":
        save_module_baseline()
    else:
        run_scan()


if __name__ == "__main__":
    main()
