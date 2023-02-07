-- Initialize crime table

-- CREATE TABLE crime (
--     [date] DATETIME NULL,
--     district INT NULL,
--     [block] NVARCHAR(MAX) NULL,
--     latitude REAL NULL,
--     [description] NVARCHAR(100) NULL,
--     location_description NVARCHAR(100) NULL,
--     updated_on DATETIME NULL,
--     community_area INT NULL,
--     iucr NVARCHAR(MAX) NULL,
--     ward INT NULL,
--     case_number NVARCHAR(MAX) NULL,
--     [year] NVARCHAR(MAX) NULL,
--     domestic BIT NULL,
--     fbi_code NVARCHAR(MAX) NULL,
--     longitude REAL NULL,
--     beat INT NULL,
--     primary_type NVARCHAR(MAX) NULL,
--     arrest BIT NULL,
--     id INT NOT NULL PRIMARY KEY
-- );
-- GO

-- Import 2023 crime data csv into temp table using import wizard

-- Insert entries into main crime table
-- INSERT INTO crime(
--     [date], district, [block], latitude, [description], 
--     location_description, updated_on, community_area,
--     iucr, ward, case_number, [year], domestic, fbi_code, 
--     longitude, beat, primary_type, arrest, id
-- )
--     SELECT
--         [date], district, [block], latitude, [description], 
--         location_description, updated_on, community_area,
--         iucr, ward, case_number, [year], domestic, fbi_code, 
--         longitude, beat, primary_type, arrest, id
--     FROM dbo.crimes2013
-- GO

-- Drop table, repeat for 2022-2013
-- DROP TABLE dbo.crimes2013

-- Q1: Grouping number of crimes by type
SELECT 
    primary_type,
    count(primary_type) AS number_of_crimes
FROM crime
GROUP BY primary_type

-- Removing column variants 'non - criminal' and 'crim sexual assault' 
UPDATE crime
SET primary_type = 'non-criminal'
WHERE primary_type = 'non - criminal'

UPDATE crime
SET primary_type = 'criminal sexual assault'
WHERE primary_type = 'crim sexual assault'

-- Q2: Crimes and their locations for mapping
SELECT 
    primary_type, 
    LEFT([date], 6) AS [day],
    longitude,
    latitude
FROM crime
WHERE [year] = 2023
ORDER BY LEFT([date], 6) DESC;

-- Q3: Type and number of crimes per neighborhood split by whether domestic
-- This caused the merge to be over 15 million rows so we don't use this and
-- instead refactor into a more condensed query 4
SELECT 
    primary_type, 
    community_area, 
    domestic, 
    count(primary_type) AS num_crimes
FROM crime
WHERE year = 2022
GROUP BY primary_type, community_area, domestic

-- Q4: Number of crimes per neighborhood
SELECT 
    community_area,
    count(community_area) AS num_crimes
FROM crime
WHERE community_area IS NOT NULL
GROUP BY community_area
ORDER BY community_area