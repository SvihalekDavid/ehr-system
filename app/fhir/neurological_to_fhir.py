from datetime import datetime

def neurological_symptoms_to_fhir(record, patient=None, user=None):
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

    if record.headache is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "25064002",
                    "display": "Headache"
                }]
            },
            "valueBoolean": record.headache
        })
    if record.dizziness is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "404640003",
                    "display": "Dizziness"
                }]
            },
            "valueBoolean": record.dizziness
        })
    if record.balance_issues is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "387603000",
                    "display": "Balance impairment"
                }]
            },
            "valueBoolean": record.balance_issues
        })
    if record.consciousness_issues is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "SNOMED CT",
                    "code": "271594007",
                    "display": "Altered level of consciousness"
                }]
            },
            "valueBoolean": record.consciousness_issues
        })
    if record.drunk_feeling is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "Local",
                    "code": "–",
                    "display": "Feeling of drunkenness"
                }]
            },
            "valueBoolean": record.drunk_feeling
        })
    if record.headache_type:
        fhir["component"].append({
            "code": {"text": "Headache Type"},
            "valueString": record.headache_type
        })

    if record.intensity is not None:
        fhir["component"].append({
            "code": {"text": "Intensity"},
            "valueInteger": record.intensity
        })

    return fhir
