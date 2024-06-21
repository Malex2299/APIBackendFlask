USE contactos_db;

DROP TABLE IF EXISTS contacts;

select * from contacto;

INSERT INTO contacto (nombre, apellido, telefono, pais) VALUES
('Carlos', 'Hernandez', '50212345678', 'Guatemala'),
('Ana', 'Lopez', '50287654321', 'Guatemala'),
('Luis', 'Martinez', '50223456789', 'Guatemala'),
('Maria', 'Gomez', '50234567890', 'Guatemala'),
('Jose', 'Perez', '50245678901', 'Guatemala'),
('Elena', 'Ramirez', '50256789012', 'Guatemala'),
('John', 'Doe', '1234567890', 'USA'),
('Jane', 'Smith', '0987654321', 'Canada'),
('Michael', 'Brown', '1112223333', 'UK'),
('Emily', 'Davis', '4445556666', 'Australia'),
('Chris', 'Wilson', '7778889999', 'New Zealand'),
('Jessica', 'Taylor', '2223334444', 'Ireland'),
('Daniel', 'Lee', '5556667777', 'Singapore'),
('Sarah', 'Martinez', '8889990000', 'Spain'),
('David', 'Clark', '3334445555', 'Germany');

CREATE TABLE contacto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    telefono VARCHAR(20),
    pais VARCHAR(50)
);

