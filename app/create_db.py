import sqlite3
import os

def create_database():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/ehr.db")
    cursor = conn.cursor()

    cursor.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS organisation (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT
);

CREATE TABLE IF NOT EXISTS user (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    organisation_id TEXT,
    FOREIGN KEY (organisation_id) REFERENCES organisation(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS patient (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date DATE NOT NULL,
    sex TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eeg_record (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    user_id TEXT,
    timestamp DATETIME NOT NULL,
    eeg_type TEXT,
    dominant_frequency REAL,
    abnormal_rhythms BOOLEAN,
    abnormal_rhythm_type TEXT,
    technician_comment TEXT,
    version INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS alcohol_intake (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    user_id TEXT,
    timestamp DATETIME NOT NULL,
    alcohol_type TEXT,
    amount_units REAL,
    frequency TEXT,
    audit_score INTEGER,
    version INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS neurological_symptoms (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    user_id TEXT,
    timestamp DATETIME NOT NULL,
    headache BOOLEAN,
    headache_type TEXT,
    intensity INTEGER,
    dizziness BOOLEAN,
    balance_issues BOOLEAN,
    consciousness_issues BOOLEAN,
    drunk_feeling BOOLEAN,
    version INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS clinical_exam (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    user_id TEXT,
    timestamp DATETIME NOT NULL,
    gcs INTEGER,
    orientation BOOLEAN,
    arm_strength TEXT,
    leg_strength TEXT,
    clinical_note TEXT,
    version INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS vital_signs (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    user_id TEXT,
    timestamp DATETIME NOT NULL,
    temperature REAL,
    bp_systolic INTEGER,
    bp_diastolic INTEGER,
    heart_rate INTEGER,
    version INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE IF NOT EXISTS social_background (
    id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    user_id TEXT,
    timestamp DATETIME NOT NULL,
    occupation TEXT,
    lifestyle TEXT,
    sleep_pattern TEXT,
    sleep_duration REAL,
    version INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (patient_id) REFERENCES patient(id),
    FOREIGN KEY (user_id) REFERENCES user(id)
);
""")

    conn.commit()
    conn.close()
    print("Databáze byla úspěšně vytvořena jako data/ehr.db")

if __name__ == "__main__":
    create_database()
