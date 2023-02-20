-- Write your own SQL object definition here, and it'll be included in your package.
DROP DATABASE ETLDEMO
GO

CREATE DATABASE ETLDEMO
USE ETLDEMO

DROP Table IF EXISTS Expenses

CREATE TABLE Expenses(
    [date] DATETIME,
    USD money,
    rate DECIMAL(6,5),
    CAD money)

    