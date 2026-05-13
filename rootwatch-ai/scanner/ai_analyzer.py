import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def shorten_text(text, max_chars=700):
    if not text:
        return "Not available"

    text = str(text).strip()

    if len(text) <= max_chars:
        return text

    return text[:max_chars] + "\n...[truncated]"


def local_fallback_analysis(evidence):
    module = evidence.get("module", "unknown")
    modinfo = evidence.get("modinfo", "").lower()

    if "modinfo not available" in modinfo:
        classification = "Unknown"
        risk = "Medium"
        explanation = (
            "This module was not present in the clean baseline and modinfo metadata "
            "is not available. It may be a manually inserted local module and should be investigated."
        )
    else:
        classification = "Needs Review"
        risk = "Low/Medium"
        explanation = (
            "This module has metadata but was not present in the clean baseline. "
            "It may be legitimate if recently installed, but it should be verified."
        )

    return f"""
Classification: {classification}
Risk Level: {risk}

Explanation:
{explanation}

Recommended Actions:
1. Verify whether this module was expected.
2. Check who loaded it using auditd logs.
3. Review module path and metadata.
4. Remove the module if unauthorized.

Note: Local fallback analysis used because AI API was unavailable or quota-limited.
"""


def analyze_module_with_ai(evidence):
    if not GEMINI_API_KEY:
        return local_fallback_analysis(evidence)

    client = genai.Client(api_key=GEMINI_API_KEY)

    module_name = evidence.get("module", "unknown")
    lsmod_output = shorten_text(evidence.get("lsmod"), 250)
    proc_output = shorten_text(evidence.get("proc_modules"), 250)
    modinfo_output = shorten_text(evidence.get("modinfo"), 700)

    prompt = f"""
You are a SOC analyst. Analyze this newly detected Linux kernel module.

Reason for alert:
The module was not present in the clean baseline.

Module:
{module_name}

lsmod:
{lsmod_output}

proc_modules:
{proc_output}

modinfo:
{modinfo_output}

Return only:
Classification: Likely Legitimate / Unknown / Suspicious
Risk: Low / Medium / High
Explanation: 2-3 sentences
Recommended actions: 3 bullets

Do not say it is definitely a rootkit. Base your answer only on the evidence.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return local_fallback_analysis(evidence) + f"\nAI API Error: {e}"
