CREATE TABLE IF NOT EXISTS doctors (
    id VARCHAR(16) PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    email VARCHAR(100) UNIQUE
);

INSERT INTO doctors (id, name, surname, email) VALUES
("0000000000000000", "Mario", "Rossi", "rossi@example.com"),
("1111111111111111", "Anna", "Bianchi", "bianchi@example.com");