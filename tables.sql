Create Covid19DailyData Database
Create Database Covid19DailyData;
USE Covid19DailyData;

CREATE TABLE DailyData (
    ReportDate DATE Primary Key,
    Cases INT,
    Deaths INT,
    Hospitalizations INT

);