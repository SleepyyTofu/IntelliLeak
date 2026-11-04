# Calculate overall risk score

def calculate_risk(

    findings,
    similarity_results=None

):

    total_score = 0

    # Risk weights
    risk_weights = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 4,
        "CRITICAL": 6
    }

    # ==========================
    # DLP Risk Score
    # ==========================

    for item in findings:

        risk_level = item["risk"]

        total_score += risk_weights.get(
            risk_level,
            0
        )

    # ==========================
    # Semantic Similarity Risk
    # ==========================

    # Only contribute similarity risk when
    # sensitive information has already been detected.

    if findings and similarity_results:

        top_similarity = similarity_results[0]["similarity"]

        if top_similarity >= 80:

            total_score += 2

        elif top_similarity >= 60:

            total_score += 1

    # ==========================
    # Final Classification
    # ==========================

    if total_score == 0:

        overall_risk = "SAFE"

    elif total_score <= 3:

        overall_risk = "LOW"

    elif total_score <= 7:

        overall_risk = "MEDIUM"

    elif total_score <= 12:

        overall_risk = "HIGH"

    else:

        overall_risk = "CRITICAL"


    # Escalate if highly sensitive data exists

    if any(item["risk"] == "CRITICAL" for item in findings):

        overall_risk = "CRITICAL"

    elif any(item["risk"] == "HIGH" for item in findings):

        overall_risk = "HIGH"

    return total_score, overall_risk