from datetime import datetime

def social_background_to_fhir(record):
    fhir = {
        "resourceType": "Observation",
        "id": record.id,
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "social-history",
                "display": "Social History"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "LG41762-2",
                "display": "Social background"
            }],
            "text": "Social background"
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

    if record.occupation:
        fhir["component"].append({
            "code": {"text": "Occupation"},
            "valueString": record.occupation
        })

    if record.lifestyle:
        fhir["component"].append({
            "code": {"text": "Lifestyle"},
            "valueString": record.lifestyle
        })

    if record.sleep_pattern:
        fhir["component"].append({
            "code": {"text": "Sleep Pattern"},
            "valueString": record.sleep_pattern
        })

    if record.sleep_duration is not None:
        fhir["component"].append({
            "code": {"text": "Sleep Duration"},
            "valueQuantity": {
                "value": record.sleep_duration,
                "unit": "hours"
            }
        })

    return fhir
