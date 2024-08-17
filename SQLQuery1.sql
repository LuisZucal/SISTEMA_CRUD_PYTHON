CREATE DATABASE python_crud;
GO

USE python_crud;  

CREATE TABLE items (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100) NOT NULL,
    description NVARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL
);

CREATE TABLE file_uploads (
    id INT PRIMARY KEY IDENTITY(1,1),
    filename NVARCHAR(255),
    upload_date DATETIME,
    product_count INT
);