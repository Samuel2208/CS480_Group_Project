-- Drop tables if they exist for a clean reset
DROP TABLE IF EXISTS Review, Rent, ClientAddress, CreditCard, DriverModel, Driver, Client, Manager, Model, Car, Address CASCADE;

-- Enum for transmission type
DROP TYPE IF EXISTS transmission_type CASCADE;
CREATE TYPE transmission_type AS ENUM ('manual', 'automatic');

-- ====================
-- Address
-- ====================
CREATE TABLE Address (
    address_id SERIAL PRIMARY KEY,
    street VARCHAR(100) NOT NULL,
    number VARCHAR(10) NOT NULL,
    city VARCHAR(100) NOT NULL
);

-- ====================
-- Manager
-- ====================
CREATE TABLE Manager (
    ssn VARCHAR(11) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE
);

-- ====================
-- Client
-- ====================
CREATE TABLE Client (
    client_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- ====================
-- Client Addresses (1..*)
-- ====================
CREATE TABLE ClientAddress (
    client_id INT REFERENCES Client(client_id) ON DELETE CASCADE,
    address_id INT REFERENCES Address(address_id) ON DELETE CASCADE,
    PRIMARY KEY (client_id, address_id)
);

-- ====================
-- Credit Card
-- ====================
CREATE TABLE CreditCard (
    card_number VARCHAR(20) PRIMARY KEY,
    client_id INT REFERENCES Client(client_id) ON DELETE CASCADE,
    payment_address_id INT REFERENCES Address(address_id) NOT NULL
);

-- ====================
-- Car
-- ====================
CREATE TABLE Car (
    car_id SERIAL PRIMARY KEY,
    brand VARCHAR(100) NOT NULL
);

-- ====================
-- Model (1:1 with Car)
-- ====================
CREATE TABLE Model (
    car_id INT REFERENCES Car(car_id) ON DELETE CASCADE,
    model_id INT NOT NULL,
    color VARCHAR(50) NOT NULL,
    construction_year INT NOT NULL,
    transmission transmission_type NOT NULL,
    PRIMARY KEY (car_id, model_id)
);

-- ====================
-- Driver
-- ====================
CREATE TABLE Driver (
    driver_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    address_id INT REFERENCES Address(address_id) NOT NULL
);

-- ====================
-- Driver-Model Mapping (many-to-many)
-- ====================
CREATE TABLE DriverModel (
    driver_id INT REFERENCES Driver(driver_id) ON DELETE CASCADE,
    car_id INT NOT NULL,
    model_id INT NOT NULL,
    PRIMARY KEY (driver_id, car_id, model_id),
    FOREIGN KEY (car_id, model_id) REFERENCES Model(car_id, model_id) ON DELETE CASCADE
);

-- ====================
-- Rent
-- ====================
CREATE TABLE Rent (
    rent_id SERIAL PRIMARY KEY,
    rent_date DATE NOT NULL,
    client_id INT REFERENCES Client(client_id) NOT NULL,
    driver_id INT REFERENCES Driver(driver_id) NOT NULL,
    car_id INT NOT NULL,
    model_id INT NOT NULL,
    FOREIGN KEY (car_id, model_id) REFERENCES Model(car_id, model_id) ON DELETE CASCADE,
    UNIQUE (rent_date, driver_id),
    UNIQUE (rent_date, car_id)
);

-- ====================
-- Review
-- ====================
CREATE TABLE Review (
    review_id SERIAL PRIMARY KEY,
    driver_id INT REFERENCES Driver(driver_id) ON DELETE CASCADE,
    client_id INT REFERENCES Client(client_id) ON DELETE CASCADE,
    rent_id INT REFERENCES Rent(rent_id) ON DELETE CASCADE,
    message TEXT,
    rating INT CHECK (rating >= 0 AND rating <= 5),
    UNIQUE (driver_id, client_id, rent_id)
);
