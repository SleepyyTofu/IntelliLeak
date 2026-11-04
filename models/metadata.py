"""
Metadata Comparison Module
Used for metadata-assisted attribution.
"""

from models.reference_metadata import REFERENCE_METADATA


def compare_metadata(uploaded_metadata, document_name):

    """
    Compare uploaded metadata against
    reference document metadata.
    """

    if not uploaded_metadata:

        return {

            "matched": False,

            "score": 0,

            "reason": "No metadata available"

        }

    reference = REFERENCE_METADATA.get(
        document_name,
        {}
    )

    if not reference:

        return {

            "matched": False,

            "score": 0,

            "reason": "Reference metadata not found"

        }

    score = 0

    matches = []

    # Compare Author ↔ Owner
    author = str(
        uploaded_metadata.get("Author", "")
    ).lower()

    owner = str(
        reference.get("owner", "")
    ).lower()

    if author and owner:

        if author == owner:

            score += 50

            matches.append(
                "Author matches Owner"
            )

    # Compare Title ↔ Department
    title = str(
        uploaded_metadata.get("Title", "")
    ).lower()

    department = str(
        reference.get("department", "")
    ).lower()

    if title and department:

        if department in title:

            score += 50

            matches.append(
                "Department matches Title"
            )

    return {

        "matched": score > 0,

        "score": score,

        "matches": matches

    }