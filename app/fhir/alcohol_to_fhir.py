from datetime import datetime

def alcohol_intake_to_fhir(record, patient=None, user=None):
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
                "display": "Alcohol intake panel"
            }],
            "text": "Alcohol consumption"
        },
        "subject": {
            "reference": f"Patient/{record.patient_id}",
            "display": patient.name if patient else "Unknown Patient"
        },
        "effectiveDateTime": record.timestamp.isoformat(),
        "issued": record.created_at.isoformat() if record.created_at else datetime.now().isoformat(),
        "performer": [{
            "reference": f"Practitioner/{record.user_id}" if record.user_id else "Practitioner/unknown",
            "display": user.name if user else "Unknown Practitioner"
        }],
        "component": []
    }

    if record.amount_units is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "228313008",
                    "display": "Units of alcohol consumed per week"
                }]
            },
            "valueQuantity": {
                "value": record.amount_units,
                "unit": "units"
            }
        })

    if record.frequency:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "289152009",
                    "display": "Drinking frequency"
                }]
            },
            "valueString": record.frequency
        })

    if record.alcohol_type:
        fhir["component"].append({
            "code": {"text": "Type"},
            "valueString": record.alcohol_type
        })

    if record.audit_score is not None:
        fhir["component"].append({
            "code": {"text": "AUDIT Score"},
            "valueInteger": record.audit_score
        })

    return fhir
