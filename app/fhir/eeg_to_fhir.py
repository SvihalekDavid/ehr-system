from datetime import datetime

def eeg_record_to_fhir(record):
    fhir = {
        "resourceType": "Observation",
        "id": record.id,
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "procedure",
                "display": "Procedure"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "LP6239-0",
                "display": "Electroencephalogram"
            }],
            "text": "Electroencephalogram"
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

    if record.eeg_type:
        fhir["component"].append({
            "code": {"text": "EEG Type"},
            "valueString": record.eeg_type
        })

    if record.dominant_frequency is not None:
        fhir["component"].append({
            "code": {"text": "Dominant Frequency"},
            "valueQuantity": {
                "value": record.dominant_frequency,
                "unit": "Hz"
            }
        })

    if record.abnormal_rhythms is not None:
        fhir["component"].append({
            "code": {"text": "Abnormal Rhythms"},
            "valueBoolean": record.abnormal_rhythms
        })

    if record.abnormal_rhythm_type:
        fhir["component"].append({
            "code": {"text": "Abnormal Rhythm Type"},
            "valueString": record.abnormal_rhythm_type
        })

    if record.technician_comment:
        fhir["component"].append({
            "code": {"text": "Technician Comment"},
            "valueString": record.technician_comment
        })

    return fhir
