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
    explanation TEXT NOT NULL            -- Explainability details
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
    report_id INTEGER                   -- Optional associated report
);