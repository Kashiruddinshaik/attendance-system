CREATE DATABASE face_recognition_db;

USE face_recognition_db;

CREATE TABLE faces (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image LONGBLOB NOT NULL
);
