import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Allow dashboard/app.py to import scanner modules from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from scanner.module_check import check_module_changes
from scanner.module_details import collect_module_evidence
from scanner.ai_analyzer import analyze_module_with_ai


st.set_page_config(
    page_title="RootWatch AI Dashboard",
    layout="wide"
)

st.title("RootWatch AI")
st.caption("Linux Kernel Module Baseline Scanner with AI-Assisted SOC Analysis")


def get_findings():
    return check_module_changes()


def risk_score(findings):
    score = 0

    for finding in findings:
        risk = finding.get("risk", "").lower()

        if risk == "high":
            score += 3
        elif risk == "medium":
            score += 2
        elif risk == "low":
            score += 1

    return score


def risk_label(score):
    if score >= 5:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"


findings = get_findings()
score = risk_score(findings)
overall_risk = risk_label(score)

new_modules = [
    f for f in findings
    if f.get("type") == "New Kernel Module"
]

removed_modules = [
    f for f in findings
    if f.get("type") == "Removed Kernel Module"
]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Findings", len(findings))
col2.metric("New Modules", len(new_modules))
col3.metric("Removed Modules", len(removed_modules))
col4.metric("Overall Risk", overall_risk)

st.divider()

if not findings:
    st.success("No suspicious kernel module changes found.")
    st.info("Your current loaded kernel modules match the saved clean baseline.")
    st.stop()


st.subheader("Findings Summary")

summary_df = pd.DataFrame(findings)
st.dataframe(summary_df, use_container_width=True)

st.divider()

st.subheader("Finding Details")

for index, finding in enumerate(findings, start=1):
    finding_type = finding.get("type", "Unknown")
    risk = finding.get("risk", "Unknown")
    reason = finding.get("reason", "No reason provided")
    module_name = finding.get("name", "N/A")

    with st.expander(f"{index}. {finding_type} — {module_name} — Risk: {risk}", expanded=True):
        st.write("**Type:**", finding_type)
        st.write("**Risk:**", risk)
        st.write("**Reason:**", reason)

        if "name" in finding:
            st.write("**Module Name:**", module_name)

        if finding_type == "New Kernel Module":
            evidence = collect_module_evidence(module_name)

            st.markdown("### Evidence")

            st.markdown("**lsmod output:**")
            st.code(evidence.get("lsmod", "Not available"))

            st.markdown("**/proc/modules output:**")
            st.code(evidence.get("proc_modules", "Not available"))

            st.markdown("**modinfo output:**")
            st.code(evidence.get("modinfo", "Not available"))

            st.markdown("### AI Analysis")

            if st.button(f"Generate AI Analysis for {module_name}", key=f"ai_{module_name}_{index}"):
                with st.spinner("Analyzing module with AI..."):
                    ai_result = analyze_module_with_ai(evidence)
                    st.write(ai_result)

st.divider()

st.subheader("How RootWatch AI Works")

st.code(
    """
Clean baseline modules
        ↓
Current loaded modules
        ↓
Compare baseline vs current
        ↓
Detect new or removed modules
        ↓
Collect evidence using lsmod, /proc/modules, modinfo
        ↓
AI explains whether the module appears legitimate, unknown, or suspicious
    """,
    language="text"
)

st.info(
    "RootWatch AI does not claim a module is definitely malicious. "
    "It identifies kernel module changes and provides investigation guidance."
)
