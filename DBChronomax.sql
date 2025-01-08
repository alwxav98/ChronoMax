USE Chronomax;
GO

CREATE TABLE Activities (
    ID INT IDENTITY(1,1) PRIMARY KEY, -- Clave primaria única para cada actividad
    UserID INT NOT NULL,              -- Relación con la tabla Users
    ActivityName NVARCHAR(255) NOT NULL, -- Nombre de la actividad
    Duration INT NOT NULL,            -- Duración de la actividad en segundos
    ActivityDate DATETIME DEFAULT GETDATE(), -- Fecha y hora en que se realizó la actividad
    FOREIGN KEY (UserID) REFERENCES Users(ID) ON DELETE CASCADE -- Relación con Users y eliminación en cascada
);
GO

select * from Users
select * from Activities
select * from cronometro

drop table cronometro
