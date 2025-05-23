from datetime import datetime

def clinical_exam_to_fhir(record):
    fhir = {
        "resourceType": "Observation",
        "id": record.id,
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "exam",
                "display": "Exam"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "29545-1",  # Example LOINC code for physical findings
                "display": "Physical findings"
            }],
            "text": "Clinical examination"
        },
        "subject": {
            "reference": f"Patient/{record.patient_id}"
        },
        "effectiveDateTime": record.timestamp.isoformat(),
        "issued": record.created_at.isoformat() if record.created_at else datetime.now().isoformat(),
        "performer": [{
            "reference": f"Practitioner/{record.user_id}" if record.user_id else "Practitioner/unknown"
        }],
        "component": []
    }

    if record.gcs is not None:
        fhir["component"].append({"code": {"text": "GCS"}, "valueInteger": record.gcs})
    fhir["component"].append({"code": {"text": "Orientation"}, "valueBoolean": record.orientation})
    if record.arm_strength:
        fhir["component"].append({"code": {"text": "Arm Strength"}, "valueString": record.arm_strength})
    if record.leg_strength:
        fhir["component"].append({"code": {"text": "Leg Strength"}, "valueString": record.leg_strength})
    if record.clinical_note:
        fhir["component"].append({"code": {"text": "Clinical Note"}, "valueString": record.clinical_note})

    return fhir
