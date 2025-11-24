CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS patients (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_cf VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER NOT NULL REFERENCES doctors(id),
    patient_id INTEGER REFERENCES patients(id),
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

INSERT INTO doctors (name, surname, email, hashed_password) 
VALUES 
    ('Mario', 'Rossi', 'rossi@doctors.com', 'doctor_hashed_password1'),
    ('Giovanni', 'Bianchi', 'bianchi@doctors.com', 'doctor_hashed_password2'),
    ('Luca', 'Verdi', 'verdi@doctors.com', 'doctor_hashed_password3'),
    ('Anna', 'Neri', 'neri@doctors.com', 'doctor_hashed_password4');

INSERT INTO patients (name, surname, email, hashed_cf)
VALUES
    ('Alessandro', 'Romano', 'romano@patients.com', 'hashed_cf_1'),
    ('Francesca', 'Galli', 'galli@patients.com', 'hashed_cf_2'),
    ('Giulia', 'Costa', 'costa@patients.com', 'hashed_cf_3'),
    ('Matteo', 'Ferrari', 'ferrari@patients.com', 'hashed_cf_4');

INSERT INTO logs (doctor_id, patient_id, description)
VALUES
    (1, 1, 'Controllo annuale'),
    (1, 2, 'Visita di follow-up'),
    (2, NULL, 'Aggiornamento cartella clinica'),
    (3, 3, 'Visita specialistica'),
    (4, NULL, 'Teleconsulto'),
    (2, 4, 'Vaccinazione'),
    (3, NULL, 'Revisione documenti medici');