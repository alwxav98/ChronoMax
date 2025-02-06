CREATE DATABASE Chronomax;
GO
USE Chronomax;
GO
CREATE TABLE Users (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    Email NVARCHAR(50) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    CreatedAt DATETIME DEFAULT GETDATE()
);

select * from Users

USE Chronomax;
GO

CREATE TABLE Activities (
    ID INT IDENTITY(1,1) PRIMARY KEY, -- Clave primaria �nica para cada actividad
    UserID INT NOT NULL,              -- Relaci�n con la tabla Users
    ActivityName NVARCHAR(50) NOT NULL, -- Nombre de la actividad
    Duration INT NOT NULL,            -- Duraci�n de la actividad en segundos
    ActivityDate DATETIME DEFAULT GETDATE(), -- Fecha y hora en que se realiz� la actividad
    FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE -- Relaci�n con Users y eliminaci�n en cascada
);
GO

select * from Users
select * from Activities
select * from cronometro

drop table cronometro
