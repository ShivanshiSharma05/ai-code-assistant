from analyzer import analyze_code


# ==================================================
# RISK CALCULATION
# ==================================================

def calculate_risk(analysis, file_content):

    risk_score = 0
    risk_reasons = []

    quality_score = analysis.get("quality_score", 5)
    complexity = analysis.get("complexity", "O(1)")
    bugs = analysis.get("bugs", "")

    lines = file_content.splitlines()
    line_count = len(lines)

    # ==================================================
    # QUALITY SCORE ANALYSIS
    # ==================================================

    if quality_score <= 4:

        risk_score += 4

        risk_reasons.append(
            "Low code quality score"
        )

    elif quality_score <= 7:

        risk_score += 2

        risk_reasons.append(
            "Moderate code quality score"
        )

    # ==================================================
    # COMPLEXITY ANALYSIS
    # ==================================================

    high_complexity = [
        "O(n^2)",
        "O(n²)",
        "O(n^3)",
        "O(n³)",
        "O(2^n)",
        "O(n!)"
    ]

    if complexity in high_complexity:

        risk_score += 4

        risk_reasons.append(
            f"High algorithmic complexity: {complexity}"
        )

    # O(n^k) means nested loops detected by analyzer
    elif complexity == "O(n^k)":

        risk_score += 3

        risk_reasons.append(
            "Nested loop complexity detected"
        )

    elif complexity == "O(n log n)":

        risk_score += 2

        risk_reasons.append(
            "Moderate algorithmic complexity detected"
        )

    # ==================================================
    # FILE SIZE ANALYSIS
    # ==================================================

    if line_count > 500:

        risk_score += 3

        risk_reasons.append(
            f"Large file detected ({line_count} lines)"
        )

    elif line_count > 250:

        risk_score += 2

        risk_reasons.append(
            f"Medium-large file detected ({line_count} lines)"
        )

    # ==================================================
    # NESTED LOOP DETECTION
    # ==================================================

    loop_indents = []
    loop_count = 0

    for line in lines:

        stripped = line.lstrip()

        if (
            stripped.startswith("for ")
            or stripped.startswith("while ")
        ):

            loop_count += 1

            indent = len(line) - len(stripped)

            loop_indents.append(indent)

    # Detect deep nesting

    if len(loop_indents) >= 3:

        max_indent = max(loop_indents)

        # Three or more loops with deep indentation
        if max_indent >= 8:

            risk_score += 4

            risk_reasons.append(
                "Deeply nested loops detected"
            )

        else:

            risk_score += 3

            risk_reasons.append(
                "Multiple nested loops detected"
            )

    elif len(loop_indents) >= 2:

        risk_score += 2

        risk_reasons.append(
            "Nested loop structure detected"
        )

    # ==================================================
    # BUG DETECTION
    # ==================================================

    bugs_lower = str(bugs).lower()

    safe_messages = [
        "no syntax errors",
        "no errors",
        "looks good",
        "no issues"
    ]

    is_safe = any(
        message in bugs_lower
        for message in safe_messages
    )

    issue_keywords = [
        "error",
        "bug",
        "exception",
        "warning",
        "issue"
    ]

    has_issue = any(
        keyword in bugs_lower
        for keyword in issue_keywords
    )

    if has_issue and not is_safe:

        risk_score += 3

        risk_reasons.append(
            "Potential code issue detected"
        )

    # ==================================================
    # RISK CLASSIFICATION
    # ==================================================

    if risk_score >= 7:

        risk_level = "HIGH"

    elif risk_score >= 3:

        risk_level = "MEDIUM"

    else:

        risk_level = "LOW"

    # ==================================================
    # RECOMMENDATION ENGINE
    # ==================================================

    if risk_level == "HIGH":

        recommendation = (
            "Fix immediately. This file has high complexity "
            "or deeply nested logic that may affect "
            "performance and maintainability."
        )

    elif risk_level == "MEDIUM":

        recommendation = (
            "Improve soon. Review algorithmic complexity "
            "and simplify nested logic where possible."
        )

    else:

        recommendation = (
            "Healthy file. No immediate action is required."
        )

    # ==================================================
    # RETURN RESULT
    # ==================================================

    return {

        "risk_level": risk_level,

        "risk_score": risk_score,

        "priority_score": risk_score,

        "risk_reasons": risk_reasons,

        "recommendation": recommendation,

        "line_count": line_count,

        "loop_count": loop_count
    }


# ==================================================
# ANALYZE ALL FILES
# ==================================================

def analyze_repository_files(files):

    results = {}

    for file_name, file_content in files.items():

        try:

            # Existing analyzer
            analysis = analyze_code(file_content)

            # New risk engine
            risk_data = calculate_risk(
                analysis,
                file_content
            )

            # Combine both
            results[file_name] = {
                **analysis,
                **risk_data
            }

        except Exception as e:

            results[file_name] = {

                "bugs": f"Analysis failed: {str(e)}",

                "complexity": "Unknown",

                "optimization": "Manual review required",

                "quality_score": 0,

                "risk_level": "HIGH",

                "risk_score": 10,

                "priority_score": 10,

                "risk_reasons": [
                    "Automatic analysis failed"
                ],

                "recommendation": (
                    "Manual review required because "
                    "automatic analysis failed."
                ),

                "line_count": len(
                    file_content.splitlines()
                ),

                "loop_count": 0
            }

    return results


# ==================================================
# REPOSITORY SUMMARY
# ==================================================

def calculate_repository_summary(results):

    high_risk = 0
    medium_risk = 0
    low_risk = 0

    for file_name, analysis in results.items():

        risk_level = analysis.get(
            "risk_level",
            "LOW"
        )

        if risk_level == "HIGH":

            high_risk += 1

        elif risk_level == "MEDIUM":

            medium_risk += 1

        else:

            low_risk += 1

    return {

        "total_files": len(results),

        "high_risk": high_risk,

        "medium_risk": medium_risk,

        "low_risk": low_risk
    }