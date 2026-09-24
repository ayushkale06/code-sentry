import re

def scan_vulnerabilities(code_snippet: str, language_hint: str = "") -> list[dict]:
    """
    Scans a code snippet for common security vulnerabilities using heuristics.

    Args:
        code_snippet: The raw code string to analyze.
        language_hint: Optional hint about the programming language (e.g. 'python').

    Returns:
        A list of dictionaries, each representing a finding with 'category', 'severity', 'line_number', and 'description'.
    """
    findings = []
    lines = code_snippet.split('\n')

    # Heuristic regex patterns for common vulnerabilities
    patterns = {
        "Hardcoded Secret": (r"(?i)(api_key|password|secret|token)\s*=\s*['\"][a-zA-Z0-9_\-]+['\"]", "High"),
        "Eval/Exec Usage": (r"\b(eval|exec)\s*\(", "High"),
        "SQL Injection Risk": (r"(?i)(SELECT|INSERT|UPDATE|DELETE|DROP).*(%s|\.format\(|{.*})", "High"),
        "Insecure Subprocess": (r"subprocess\.(Popen|call|run|check_call|check_output)\(.*shell\s*=\s*True.*\)", "High"),
        "Insecure Deserialization": (r"\b(pickle\.loads\(|yaml\.load\(\s*[^,]+(?!,\s*Loader=yaml\.SafeLoader).*\))", "High"),
        "Weak Hashing": (r"\b(hashlib\.md5|hashlib\.sha1)\b", "Medium"),
    }

    for i, line in enumerate(lines, start=1):
        for category, (pattern, severity) in patterns.items():
            if re.search(pattern, line):
                findings.append({
                    "category": category,
                    "severity": severity,
                    "line_number": i,
                    "description": f"Potential {category} detected."
                })

    return findings
