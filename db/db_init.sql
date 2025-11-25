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
    description VARCHAR(100) NOT NULL,
    doctor_id INTEGER,
    patient_hashed_cf VARCHAR(255),
    data_id INTEGER,
    report_id INTEGER
);

INSERT INTO doctors (name, surname, email, hashed_password) VALUES
('Roberto', 'Carriero', 'roberto.carriero@email.com', 'hashedpassword1'),
('Luca', 'Cianci', 'luca.cianci@email.com', 'hashedpassword2'),
('Luca', 'Serio', 'luca.serio@email.com', 'hashedpassword3');

INSERT INTO logs (service, event, description, doctor_id, patient_hashed_cf, data_id, report_id) VALUES
('authentication', 'register_success', 'doctor registered successfully', NULL, NULL, NULL, NULL),
('authentication', 'register_fail', 'email already used', NULL, NULL, NULL, NULL),
('authentication', 'login_success', 'doctor logged in successfully', 101, NULL, NULL, NULL),
('authentication', 'login_fail', 'invalid credentials', 102, NULL, NULL, NULL),
('data_processing', 'data_processed', 'processed data stored in the database', NULL, NULL, 5001, NULL),
('data_processing', 'data_retrieved', 'processed data requested for analysis', NULL, NULL, 5001, NULL),
('explainable_ai', 'analysis_completed', 'report saved in the database', NULL, NULL, NULL, 9001),
('explainable_ai', 'reports_all', 'reports view required', 101, NULL, NULL, NULL),
('explainable_ai', 'reports_patient', 'reports view required for a patient', 101, 'RSSMRA80A01H501U', NULL, NULL);