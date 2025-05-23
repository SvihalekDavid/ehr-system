from datetime import datetime

def vital_signs_to_fhir(record, patient=None, user=None):
    fhir = {
        "resourceType": "Observation",
        "id": record.id,
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "vital-signs",
                "display": "Vital Signs"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "85353-1",
                "display": "Vital signs, panel"
            }],
            "text": "Vital signs"
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

    if record.temperature is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "LOINC",
                    "code": "8310-5",
                    "display": "Body temperature"
                }]
            },
            "valueQuantity": {
                "value": record.temperature,
                "unit": "°C"
            }
        })

    if record.bp_systolic is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "LOINC",
                    "code": "8480-6",
                    "display": "Systolic blood pressure"
                }]
            },
            "valueQuantity": {
                "value": record.bp_systolic,
                "unit": "mmHg"
            }
        })

    if record.bp_diastolic is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "LOINC",
                    "code": "8462-4",
                    "display": "Diastolic blood pressure"
                }]
            },
            "valueQuantity": {
                "value": record.bp_diastolic,
                "unit": "mmHg"
            }
        })

    if record.heart_rate is not None:
        fhir["component"].append({
            "code": {
                "coding": [{
                    "system": "LOINC",
                    "code": "8867-4",
                    "display": "Heart rate"
                }]
            },
            "valueQuantity": {
                "value": record.heart_rate,
                "unit": "bpm"
            }
        })

        return fhir
