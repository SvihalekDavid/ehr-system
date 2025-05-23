from datetime import datetime

def alcohol_intake_to_fhir(record):
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
                "code": "80439-3",
                "display": "Alcohol consumption panel"
            }],
            "text": "Alcohol consumption"
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

    if record.alcohol_type:
        fhir["component"].append({
            "code": {"text": "Type"},
            "valueString": record.alcohol_type
        })

    if record.amount_units is not None:
        fhir["component"].append({
            "code": {"text": "Amount (units)"},
            "valueQuantity": {
                "value": record.amount_units,
                "unit": "units"
            }
        })

    if record.frequency:
        fhir["component"].append({
            "code": {"text": "Frequency"},
            "valueString": record.frequency
        })

    if record.audit_score is not None:
        fhir["component"].append({
            "code": {"text": "AUDIT Score"},
            "valueInteger": record.audit_score
        })

    return fhir
