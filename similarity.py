from sentence_transformers import SentenceTransformer
from sentence_transformers.util import cos_sim
from models.reference_metadata import REFERENCE_METADATA
import os


MIN_SIMILARITY_THRESHOLD = 50

SEMANTIC_WEIGHT = 0.80

METADATA_WEIGHT = 0.20


# Load model once
model = SentenceTransformer(
    'all-MiniLM-L6-v2'
)


def analyze_similarity(input_text, metadata=None):

    results = []
    has_metadata = metadata is not None and len(metadata) > 0

    reference_folder = "reference_docs"

    input_embedding = model.encode(
        input_text,
        convert_to_tensor=True
    )

    for filename in os.listdir(reference_folder):

        file_path = os.path.join(
            reference_folder,
            filename
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            reference_text = file.read()

        reference_embedding = model.encode(
            reference_text,
            convert_to_tensor=True
        )

        similarity_score = float(
            cos_sim(
                input_embedding,
                reference_embedding
            )[0][0]
        )

        similarity_percentage = round(
            similarity_score * 100,
            2
        )

        if similarity_percentage >= 80:
            confidence = "HIGH"

        elif similarity_percentage >= 60:
            confidence = "MEDIUM"

        else:
            confidence = "LOW"

        results.append({
            "document": filename,
            "similarity": similarity_percentage,
            "confidence": confidence
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results

def get_top_source(similarity_results):

    if not similarity_results:

        return None

    top_result = similarity_results[0]

    similarity = top_result["similarity"]

    if similarity < MIN_SIMILARITY_THRESHOLD:

        return {

        "document": "UNKNOWN",

        "similarity": similarity,

        "confidence": "NONE",

        "attribution": "NO RELIABLE SOURCE"

        }

    if similarity >= 80:

        attribution = (
            "HIGH CONFIDENCE ATTRIBUTION"
        )

    elif similarity >= 60:

        attribution = (
            "MEDIUM CONFIDENCE ATTRIBUTION"
        )

    else:

        attribution = (
            "LOW CONFIDENCE ATTRIBUTION"
        )

    return {

        "document":
            top_result["document"],

        "similarity":
            top_result["similarity"],

        "confidence":
            top_result["confidence"],

        "attribution":
            attribution
    }