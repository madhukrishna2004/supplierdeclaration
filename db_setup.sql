CREATE DATABASE supplier_portal;

USE supplier_portal;

CREATE TABLE emails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_email VARCHAR(255),
    recipient_email VARCHAR(255),
    subject VARCHAR(255),
    body TEXT,
    sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    attachment_path1 VARCHAR(255),
    attachment_path2 VARCHAR(255)
);

CREATE TABLE uploads (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_email VARCHAR(255),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_path1 VARCHAR(255),
    file_path2 VARCHAR(255)
);
