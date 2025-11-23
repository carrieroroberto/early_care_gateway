CREATE TABLE IF NOT EXISTS doctors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL
);

INSERT INTO doctors (name, surname, email, hashed_password) 
VALUES 
    ('Mario', 'Rossi', 'rossi@doctors.com', 'doctor_hashed_password1'),
    ('Giovanni', 'Bianchi', 'bianchi@doctors.com', 'doctor_hashed_password2');