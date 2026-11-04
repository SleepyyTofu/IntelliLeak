"""
Incident Response Module
Provides response recommendations based on leakage risk.
"""


def generate_incident(overall_risk, findings, top_source):

    incident = {

        "status": "No Incident",

        "severity": overall_risk,

        "recommended_actions": [],

        "evidence": [],

        "report_required": False

    }

    if overall_risk == "SAFE":

        incident["status"] = "Closed"

        incident["recommended_actions"] = [

            "No action required."

        ]

        incident["evidence"].append(
            "No sensitive information detected."
        )
        
        return incident

    incident["status"] = "Open"

    incident["report_required"] = True

    # Evidence

    if findings:

        incident["evidence"].append(

            f"{len(findings)} sensitive item(s) detected."

        )

    if top_source and top_source["document"] != "UNKNOWN":

        incident["evidence"].append(

            f"Likely source: {top_source['document']}"

        )

    else:

        incident["evidence"].append(

            "No reliable source identified."

        )

    # Response

    if overall_risk == "LOW":

        incident["recommended_actions"] = [

            "Review detected information.",

            "Monitor future submissions."

        ]

    elif overall_risk == "MEDIUM":

        incident["recommended_actions"] = [

            "Review prompt before sharing.",

            "Notify document owner.",

            "Preserve analysis results."

        ]

    elif overall_risk == "HIGH":

        incident["recommended_actions"] = [

            "Prevent information sharing.",

            "Notify security administrator.",

            "Review document access permissions.",

            "Preserve evidence."

        ]

    elif overall_risk == "CRITICAL":

        incident["recommended_actions"] = [

            "Immediately block transmission.",

            "Escalate to incident response team.",

            "Preserve all evidence.",

            "Begin security investigation.",

            "Generate incident report."

        ]

    return incident