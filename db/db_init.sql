CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL,
    patient_hashed_cf VARCHAR(255),
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO doctors (name, surname, email, hashed_password) 
VALUES 
    ('Mario', 'Rossi', 'rossi@doctors.com', 'doctor_hashed_password1'),
    ('Giovanni', 'Bianchi', 'bianchi@doctors.com', 'doctor_hashed_password2'),
    ('Luca', 'Verdi', 'verdi@doctors.com', 'doctor_hashed_password3'),
    ('Anna', 'Neri', 'neri@doctors.com', 'doctor_hashed_password4');

INSERT INTO logs (doctor_id, patient_hashed_cf, description)
VALUES
    (1, 'hashed_cf_1', 'Analysis completed'),
    (1, 'hashed_cf_2', 'Data processed'),
    (2, NULL, 'Doctor has logged in'),
    (3, 'hashed_cf_3', 'Analysis completed'),
    (4, NULL, 'Doctor has registered'),
    (2, 'hashed_cf_2', 'Analysis completed'),
    (3, 'hashed_cf_4', 'Data procesed');