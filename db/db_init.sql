-- Table storing doctors' account information
CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,   -- Unique doctor email
    hashed_password VARCHAR(255) NOT NULL -- Secure hashed password
);

-- Table storing different types of processed patient data (numeric, text, image, signal...)
CREATE TABLE IF NOT EXISTS processed_data (
    id SERIAL PRIMARY KEY,
    type VARCHAR(20) NOT NULL,            -- Data category (e.g., numeric, text, image_rx)
    data TEXT NOT NULL,                   -- Raw or encoded data
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

-- Table storing medical reports produced by doctors
CREATE TABLE IF NOT EXISTS reports (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL,           -- Reference to the doctor who generated the report
    patient_hashed_cf VARCHAR(255) NOT NULL, -- Hashed patient identifier
    processed_data_id INTEGER NOT NULL,   -- ID of the processed data used in the report
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    strategy VARCHAR(255) NOT NULL,       -- AI or analysis method used
    diagnosis VARCHAR(255) NOT NULL,      -- Resulting diagnosis
    confidence FLOAT NOT NULL,            -- Confidence score
    explanation TEXT NOT NULL,            -- Explainability details
    CONSTRAINT fk_reports_doctor FOREIGN KEY(doctor_id) REFERENCES doctors(id)
    -- Note: processed_data_id is not referenced as FK, but could be added for stronger data integrity
);

-- Table storing logs of system events and analyses
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL,
    service VARCHAR(50) NOT NULL,        -- System or microservice name
    event VARCHAR(50) NOT NULL,          -- Type of event logged
    description VARCHAR(100) NOT NULL,   -- Short event description
    doctor_id INTEGER,                   -- Optional reference to a doctor
    patient_hashed_cf VARCHAR(255),      -- Optional patient hash involved in the log
    data_id INTEGER,                     -- Optional processed data ID
    report_id INTEGER,                   -- Optional associated report
    CONSTRAINT fk_logs_doctor FOREIGN KEY(doctor_id) REFERENCES doctors(id),
    CONSTRAINT fk_logs_report FOREIGN KEY(report_id) REFERENCES reports(id)
);

-- Sample doctors
INSERT INTO doctors (name, surname, email, hashed_password)
VALUES
('Mario', 'Rossi', 'mario.rossi@example.com', 'hashedpwd1'),
('Luisa', 'Bianchi', 'luisa.bianchi@example.com', 'hashedpwd2');

-- Sample processed data entries
INSERT INTO processed_data (type, data)
VALUES
('numeric', '{"blood_pressure": 120, "cholesterol": 180}'),
('text', 'Patient reports mild fever and cough for 2 days.'),
('image_rx', 'base64_encoded_xray_image_1'),
('signal', 'ecg_signal_sample_1'),
('numeric', '{"blood_sugar": 95, "heart_rate": 70}');

-- Sample medical reports linking doctors to patient data
INSERT INTO reports (doctor_id, patient_hashed_cf, processed_data_id, strategy, diagnosis, confidence, explanation)
VALUES
(1, 'ABC123XYZ', 1, 'numeric', 'high', 0.85, 'Top 5 features impacting risk'),
(1, 'DEF456UVW', 2, 'text', 'flu', 0.92, 'Symptoms indicate flu'),
(2, 'ABC123XYZ', 3, 'image', 'pneumonia', 0.78, 'X-ray analysis shows signs of pneumonia'),
(2, 'GHI789RST', 4, 'signal', 'arrhythmia', 0.65, 'ECG signal indicates irregular heartbeat'),
(1, 'GHI789RST', 5, 'numeric', 'low', 0.30, 'Blood test indicates low risk');

-- Log entries documenting analysis events
INSERT INTO logs (service, event, description, doctor_id, patient_hashed_cf, report_id)
VALUES
('explainable_ai', 'analysis_completed', 'Report saved in the database', 1, 'ABC123XYZ', 1),
('explainable_ai', 'analysis_completed', 'Report saved in the database', 2, 'ABC123XYZ', 3),
('explainable_ai', 'analysis_completed', 'Report saved in the database', 1, 'GHI789RST', 5);
