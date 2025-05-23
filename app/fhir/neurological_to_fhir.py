from datetime import datetime

def neurological_symptoms_to_fhir(record):
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
                "code": "54539-2",
                "display": "Neurological findings"
            }],
            "text": "Neurological symptoms"
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

    fhir["component"].append({"code": {"text": "Headache"}, "valueBoolean": record.headache})
    if record.headache_type:
        fhir["component"].append({"code": {"text": "Headache Type"}, "valueString": record.headache_type})
    if record.intensity is not None:
        fhir["component"].append({"code": {"text": "Intensity"}, "valueInteger": record.intensity})
    fhir["component"].append({"code": {"text": "Dizziness"}, "valueBoolean": record.dizziness})
    fhir["component"].append({"code": {"text": "Balance Issues"}, "valueBoolean": record.balance_issues})
    fhir["component"].append({"code": {"text": "Consciousness Issues"}, "valueBoolean": record.consciousness_issues})
    fhir["component"].append({"code": {"text": "Drunk Feeling"}, "valueBoolean": record.drunk_feeling})

    return fhir
