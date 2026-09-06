def calculate_file_risk(analysis_result):
    """
    Calculates risk level and priority score
    based on code quality and complexity.
    """

    quality_score = analysis_result.get("quality_score", 0)
    complexity = analysis_result.get("complexity", "Unknown")

    priority_score = 0
    reasons = []

    # ----------------------------------
    # QUALITY SCORE RISK
    # ----------------------------------

    if quality_score <= 4:
        priority_score += 5
        reasons.append("Low code quality score")

    elif quality_score <= 6:
        priority_score += 3
        reasons.append("Moderate code quality")

    elif quality_score <= 8:
        priority_score += 1

    # ----------------------------------
    # COMPLEXITY RISK
    # ----------------------------------

    high_complexity = [
        "O(n^2)",
        "O(n³)",
        "O(n^3)",
        "O(2^n)",
        "O(n!)",
        "O(n^k)"
    ]

    medium_complexity = [
        "O(n log n)",
        "O(nlogn)"
    ]

    if complexity in high_complexity:
        priority_score += 5
        reasons.append(f"High algorithmic complexity: {complexity}")

    elif complexity in medium_complexity:
        priority_score += 2
        reasons.append(f"Moderate complexity: {complexity}")

    # ----------------------------------
    # BUG RISK
    # ----------------------------------

    bugs = analysis_result.get("bugs", "")

    if bugs and bugs.lower() not in [
        "no syntax errors",
        "no issues detected",
        "none"
    ]:
        priority_score += 3
        reasons.append("Potential code issues detected")

    # ----------------------------------
    # RISK LEVEL
    # ----------------------------------

    if priority_score >= 7:
        risk_level = "HIGH"

    elif priority_score >= 3:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # ----------------------------------
    # RECOMMENDATION
    # ----------------------------------

    if risk_level == "HIGH":

        recommendation = (
            "Prioritize this file. Review complexity, "
            "potential bugs, and overall code quality."
        )

    elif risk_level == "MEDIUM":

        recommendation = (
            "Consider refactoring this file to improve "
            "maintainability and performance."
        )

    else:

        recommendation = (
            "No major risks detected. Maintain current "
            "code quality standards."
        )

    return {
        "risk_level": risk_level,
        "priority_score": priority_score,
        "risk_reasons": reasons,
        "recommendation": recommendation
    }