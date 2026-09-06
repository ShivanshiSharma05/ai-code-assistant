def calculate_severity(analysis):
    """
    Determine issue severity based on
    bugs, complexity, optimization and quality score.
    """

    bugs = str(analysis.get("bugs", "")).lower()
    complexity = str(analysis.get("complexity", "")).lower()
    optimization = str(analysis.get("optimization", "")).lower()
    quality_score = analysis.get("quality_score", 7)

    # Critical syntax/runtime problems
    if (
        "syntax error" in bugs
        or "error" in bugs and "no syntax errors" not in bugs
    ):
        return "CRITICAL"

    # High complexity or very low quality
    if (
        "o(n^3)" in complexity
        or "o(n^k)" in complexity
        or quality_score <= 4
    ):
        return "HIGH"

    # Moderate complexity / optimization required
    if (
        "o(n^2)" in complexity
        or (
            "optimize" in optimization
            and "looks optimal" not in optimization
        )
        or quality_score <= 6
    ):
        return "MEDIUM"

    return "LOW"


def calculate_health_score(analyses):
    """
    Calculate overall repository health score.
    Score ranges from 0 to 100.
    """

    if not analyses:
        return 0

    total_quality = 0
    severity_penalty = 0

    severity_penalties = {
        "CRITICAL": 20,
        "HIGH": 12,
        "MEDIUM": 6,
        "LOW": 1
    }

    for analysis in analyses:
        quality_score = analysis.get("quality_score", 7)

        try:
            quality_score = int(quality_score)
        except (ValueError, TypeError):
            quality_score = 7

        total_quality += quality_score

        severity = calculate_severity(analysis)

        severity_penalty += severity_penalties.get(
            severity,
            1
        )

    average_quality = total_quality / len(analyses)

    # Convert quality score from /10 to /100
    health_score = average_quality * 10

    # Penalty should not destroy the score
    health_score -= severity_penalty / len(analyses)

    health_score = max(0, min(100, round(health_score)))

    return health_score


def create_issue_summary(file_name, analysis):
    """
    Convert file analysis into a structured issue summary.
    """

    severity = calculate_severity(analysis)

    return {
        "file_name": file_name,
        "severity": severity,
        "bugs": analysis.get("bugs", ""),
        "complexity": analysis.get("complexity", ""),
        "optimization": analysis.get("optimization", ""),
        "quality_score": analysis.get("quality_score", 0)
    }


def get_repository_summary(results):
    """
    Generate complete repository intelligence summary.
    """

    analyses = list(results.values())

    health_score = calculate_health_score(analyses)

    issues = []

    severity_count = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0
    }

    for file_name, analysis in results.items():

        issue = create_issue_summary(
            file_name,
            analysis
        )

        severity = issue["severity"]

        severity_count[severity] += 1

        issues.append(issue)

    # Sort by severity priority
    priority_order = {
        "CRITICAL": 1,
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 4
    }

    issues.sort(
        key=lambda x: priority_order.get(
            x["severity"],
            5
        )
    )

    return {
        "repository_health_score": health_score,
        "total_files_analyzed": len(results),
        "severity_summary": severity_count,
        "issues": issues
    }