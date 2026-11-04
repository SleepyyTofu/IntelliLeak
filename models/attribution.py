"""
Hybrid Attribution Module
Combines semantic similarity and metadata evidence.
"""

MIN_ATTRIBUTION_THRESHOLD = 50


def build_attribution(top_source, metadata_result):

    if not top_source:

        return {
            "document": "UNKNOWN",
            "confidence": "NONE",
            "status": "NO SOURCE"
        }

    similarity = top_source["similarity"]

    metadata_score = metadata_result.get(
        "score",
        0
    )

    # Hybrid attribution score
    final_score = round(
        (similarity * 0.8) +
        (metadata_score * 0.2),
        2
    )

    if final_score < MIN_ATTRIBUTION_THRESHOLD:

        return {

            "document": "UNKNOWN",

            "score": final_score,

            "confidence": "NONE",

            "status": "NO RELIABLE SOURCE"

        }

    if final_score >= 80:

        confidence = "HIGH"

    elif final_score >= 60:

        confidence = "MEDIUM"

    else:

        confidence = "LOW"

    return {

        "document":
            top_source["document"],

        "score":
            final_score,

        "confidence":
            confidence,

        "status":
            "ATTRIBUTED"

    }