CREATE DATABASE PRACTICA01
GO

USE PRACTICA01
GO

CREATE TABLE SALON(
	IdSalon int PRIMARY KEY,
	NombreSalon varchar(20) DEFAULT NULL,
	Disponible BIT NOT NULL
)
GO

CREATE TABLE PROFESOR(
	DniProfesor char(8) NOT NULL UNIQUE,
	IdProfesor int IDENTITY(1,1) PRIMARY KEY,
	Nombres varchar(30) NOT NULL,
	Apellidos varchar(30) NOT NULL,
	Edad int NOT NULL,
	Estatura decimal(3,2) NOT NULL,
	Especialidad varchar(20) default NULL,
	Disponible BIT NOT NULL
)
GO

CREATE TABLE ALUMNO(
	DniAlumno char(8) NOT NULL UNIQUE,
	IdAlumno int IDENTITY(1,1) PRIMARY KEY,
	Nombres varchar(30) NOT NULL,
	Apellidos varchar(30) NOT NULL,
	Edad int NOT NULL,
	Estatura decimal(3,2) default 0,
	Genero char(1) NOT NULL	CHECK (Genero IN ('M','F')),
	Delegado int,
	IdTutor int NOT NULL,
	IdSalon int NOT NULL,
	Disponible BIT NOT NULL,
	FOREIGN KEY (IdSalon) REFERENCES SALON(IdSalon),
	FOREIGN KEY (IdTutor) REFERENCES PROFESOR(IdProfesor),
	FOREIGN KEY (Delegado) REFERENCES ALUMNO(IdAlumno)
)
GO

ALTER TABLE	ALUMNO
	ADD IdTutor int

UPDATE ALUMNO
SET IdTutor = 1

DROP TABLE ALUMNO
DROP TABLE SALON
DROP TABLE PROFESOR

INSERT INTO SALON
VALUES 
(1, 'A101',1),
(2, null, 1),
(3, null, 1)
GO
INSERT INTO PROFESOR
VALUES 
('87654321', 'ISAIAS', 'MEDINA TAMALON', 45, 1.65, 'BASE DE DATOS', 1),
('12345677', 'MARIA', 'ROSALES ALLENDE', 30, 1.50, null, 1),
('12345688', 'LENIN', 'ARCE HUAMAN', 50, 1.60, NULL, 1)
GO
INSERT INTO ALUMNO
VALUES 
('12345678', 'PEPE', 'GRILLO', 20, 1.69, 'M', 1, 1, 1, 1),
('11111111', 'LUIS', 'GRILLO', 19, 1.73, 'M', 1, 1, 1, 1),
('22222222', 'JORGE', 'LUNA', 18, 1.60, 'M', 1, 1, 1, 1),
('22222223', 'MARIA', 'VARGAS', 18, null, 'M', 1, 1, 2, 1),
('22222224', 'SOL', 'TORRE', 18, null, 'M', 1, 3, 1, 1)
GO

SELECT * FROM SALON
SELECT * FROM PROFESOR
SELECT * FROM ALUMNO
SELECT
	A.IdAlumno AS CODIGO,
	A.Nombres AS NOMBRE,
	A.Apellidos AS APELLIDO,
	S.NombreSalon AS SALON
FROM ALUMNO AS A INNER JOIN SALON AS S
ON A.IdSalon = S.IdSalon

-- INNER JOIN
SELECT
	A.IdAlumno AS CODIGO,
	A.Nombres AS NOMBRE,
	A.Apellidos AS APELLIDO,
	S.NombreSalon AS SALON,
	P.Nombres + ' ' + P.Apellidos AS TUTOR
FROM ALUMNO AS A INNER JOIN SALON AS S
ON A.IdSalon = S.IdSalon INNER JOIN PROFESOR AS P 
ON A.IdTutor = P.IdProfesor

-- LEFT OUTER JOIN
SELECT
	A.IdAlumno AS CODIGO,
	A.Nombres + ' ' + A.Apellidos AS ALUMNO,
	S.NombreSalon AS SALON,
	P.Nombres + ' ' + P.Apellidos AS PROFESOR,
	P.Especialidad AS CURSO
FROM ALUMNO AS A LEFT OUTER JOIN SALON AS S
ON A.IdSalon = S.IdSalon LEFT OUTER JOIN PROFESOR AS P
ON A.IdTutor = P.IdProfesor 
WHERE S.NombreSalon IS NULL
--WHERE P.Especialidad IS NULL

-- RIGHT OUTER JOIN
SELECT
	A.IdAlumno AS CODIGO,
	A.Nombres + ' ' + A.Apellidos AS ALUMNO,
	S.NombreSalon AS SALON--,
	--P.Nombres + ' ' + P.Apellidos AS PROFESOR,
	--P.Especialidad AS CURSO
FROM ALUMNO AS A RIGHT OUTER JOIN SALON AS S
ON A.IdSalon = S.IdSalon-- RIGHT OUTER JOIN PROFESOR AS P
--ON A.IdTutor = P.IdProfesor 
WHERE S.NombreSalon IS NULL
--WHERE P.Especialidad IS NULL

--FUNCION SIN PARAMETROS
CREATE FUNCTION funPresente()
RETURNS VARCHAR(50)
AS
BEGIN
	DECLARE @Presente VARCHAR(50)
	SET @Presente = 'Presente profesor - Estoy en clase'
	RETURN @Presente
END

SELECT dbo.funPresente() AS PRESENTE

--FUNCION CON PARAMETROS
CREATE FUNCTION funPresenteNombre(
	@Nombre VARCHAR(80)
)
RETURNS VARCHAR(80)
AS
BEGIN
	DECLARE @Presentee VARCHAR(80)
	SET @Presentee = CONCAT('PRESENTE PROFESOR ', @Nombre, 'ESTOY EN CLASE')
	RETURN @Presentee
END
DECLARE @Nombre	VARCHAR(80)
SET @Nombre = 'ISAIAS'
SELECT dbo.funPresenteNombre(@Nombre) AS PRESENTEE

SELECT * FROM ALUMNO

SELECT
	Nombres+' '+Apellidos AS PROFESOR,
	dbo.funPresenteNombre(Nombres+' '+Apellidos) AS SALUDO
FROM PROFESOR

--FUNCION

select 
	IdAlumno as ORDEN,
	SUM(Edad) as EDAD
from ALUMNO
where IdAlumno=1
group by IdAlumno

CREATE FUNCTION funPromedioEdad(
	@Edad INT
)
RETURNS INT
BEGIN
	DECLARE @Promedio INT
	SET @Promedio= (
		
	)
	RETURN @Promedio
END


-------------------------------
CREATE FUNCTION fun_TotalAlumnosSalon(
    @IdSalon INT
)
RETURNS INT
AS
BEGIN
    DECLARE @TOTAL INT

    SET @TOTAL = (
        SELECT COUNT(*)
        FROM ALUMNO
        WHERE IdSalon = @IdSalon
    )

    RETURN @TOTAL
END

SELECT dbo.fun_TotalAlumnosSalon(X) AS 'TOTAL DE ALUMNOS'
SELECT
    IdSalon,
    dbo.fun_TotalAlumnosSalon(IdSalon) AS TOTAL_ALUMNOS
FROM SALON

-------------------
CREATE FUNCTION fun_NombreTutor(
    @IdTutor INT
)
RETURNS VARCHAR(100)
AS
BEGIN
    DECLARE @Tutor VARCHAR(100)

    SET @Tutor = (
        SELECT Nombres + ' ' + Apellidos
        FROM PROFESOR
        WHERE IdProfesor = @IdTutor
    )

    RETURN @Tutor
END
SELECT dbo.fun_NombreTutor(1)
SELECT
    Nombres + ' ' + Apellidos AS ALUMNO,
    dbo.fun_NombreTutor(IdTutor) AS TUTOR
FROM ALUMNO

---------------------------
SELECT
    AVG(Edad)
FROM ALUMNO
WHERE IdSalon = 1

CREATE FUNCTION fun_PromedioEdad(
    @IdSalon INT
)
RETURNS DECIMAL(5,2)
AS
BEGIN
    DECLARE @PROMEDIO DECIMAL(5,2)

    SET @PROMEDIO = (
        SELECT AVG(CAST(Edad AS DECIMAL(5,2)))
        FROM ALUMNO
        WHERE IdSalon = @IdSalon
    )

    RETURN @PROMEDIO
END

SELECT
    IdSalon,
    dbo.fun_PromedioEdad(IdSalon) AS PROMEDIO_EDAD
FROM SALON

---------------------------
SELECT
    IdTutor,
    COUNT(*) AS TOTAL
FROM ALUMNO
GROUP BY IdTutor

CREATE FUNCTION fun_CantidadTutorados(
    @IdTutor INT
)
RETURNS INT
AS
BEGIN
    DECLARE @TOTAL INT

    SET @TOTAL = (
        SELECT COUNT(*)
        FROM ALUMNO
        WHERE IdTutor = @IdTutor
    )

    RETURN @TOTAL
END

SELECT
    Nombres + ' ' + Apellidos AS PROFESOR,
    dbo.fun_CantidadTutorados(IdProfesor) AS TOTAL_ALUMNOS
FROM PROFESOR

COUNT()
SUM()
AVG()
MIN()
MAX()