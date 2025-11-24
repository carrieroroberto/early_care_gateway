CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

CREATE TABLE logs (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    service VARCHAR(50) NOT NULL,
    event VARCHAR(50) NOT NULL,
    
    doctor_id INTEGER,
    patient_hashed_cf VARCHAR(255),
    report_id INTEGER,
    data_id INTEGER
);

INSERT INTO logs (service, event, doctor_id, patient_hashed_cf, data_id, report_id) VALUES
('Authentication', 'LOGIN_SUCCESS', 101, NULL, NULL, NULL),
('Gateway', 'REQ_ANALYSIS', 101, 'RSSMRA80A01H501U', NULL, NULL),
('Data_Processing', 'DATA_PROCESSED', 101, 'RSSMRA80A01H501U', 5005, NULL),
('Explainable_AI', 'REPORT_SUCCESS', 101, 'RSSMRA80A01H501U', 5005, 9901),
('Explainable_AI', 'REPORTS_VIEW', 101, NULL, NULL, NULL),
('Explainable_AI', 'REPORTS_PATIENT_VIEW', 202, 'BNCLGU90B02F205Z', NULL, NULL);