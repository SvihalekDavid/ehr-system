from datetime import datetime

def vital_signs_to_fhir(record):
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
                "code": "8716-3",  # LOINC panel for vital signs
                "display": "Vital signs, panel"
            }],
            "text": "Vital signs"
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

    if record.temperature is not None:
        fhir["component"].append({
            "code": {"text": "Body Temperature"},
            "valueQuantity": {
                "value": record.temperature,
                "unit": "°C"
            }
        })

    if record.bp_systolic is not None:
        fhir["component"].append({
            "code": {"text": "Systolic Blood Pressure"},
            "valueQuantity": {
                "value": record.bp_systolic,
                "unit": "mmHg"
            }
        })

    if record.bp_diastolic is not None:
        fhir["component"].append({
            "code": {"text": "Diastolic Blood Pressure"},
            "valueQuantity": {
                "value": record.bp_diastolic,
                "unit": "mmHg"
            }
        })

    if record.heart_rate is not None:
        fhir["component"].append({
            "code": {"text": "Heart Rate"},
            "valueQuantity": {
                "value": record.heart_rate,
                "unit": "bpm"
            }
        })

    return fhir
