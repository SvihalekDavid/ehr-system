from datetime import datetime

def social_background_to_fhir(record, patient=None, user=None):
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
                "code": "75275-8",
                "display": "Social history panel"
            }],
            "text": "Social background"
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

    if record.occupation:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "14679004",
                    "display": "Occupation"
                }]
            },
            "valueString": record.occupation
        })

    if record.lifestyle:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "313204009",
                    "display": "Lifestyle"
                }]
            },
            "valueString": record.lifestyle
        })

    if record.sleep_duration is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "Local",
                    "code": "–",
                    "display": "Sleep duration"
                }]
            },
            "valueQuantity": {
                "value": record.sleep_duration,
                "unit": "hodiny"
            }
        })

    if record.sleep_pattern:
        fhir["component"].append({
            "code": {"text": "Sleep Pattern"},
            "valueString": record.sleep_pattern
        })

    return fhir
