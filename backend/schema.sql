-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS resident;
DROP TABLE IF EXISTS room;
DROP TABLE IF EXISTS floor;

-- Create floor table
CREATE TABLE floor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    level INT NOT NULL,
    name VARCHAR(255) NOT NULL
);

-- Create room table
CREATE TABLE room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    capacity INT NOT NULL,
    number INT NOT NULL,
    floor INT NOT NULL,
    FOREIGN KEY (floor) REFERENCES floor(id) ON DELETE CASCADE
);

-- Create resident table
CREATE TABLE resident (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstname VARCHAR(255) NOT NULL,
    lastname VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    room INT NOT NULL,
    FOREIGN KEY (room) REFERENCES room(id) ON DELETE CASCADE
);
