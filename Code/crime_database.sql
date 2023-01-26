-- Import 2023 data using import wizard

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

SELECT 
    primary_type,
    count(primary_type) AS number_of_crimes
FROM crime
GROUP BY primary_type

SELECT 
    primary_type, 
    LEFT([date], 6) AS [day],
    longitude,
    latitude
FROM crime
WHERE [year] = 2023

UPDATE crime
SET primary_type = 'non-criminal'
WHERE primary_type = 'non - criminal'

UPDATE crime
SET primary_type = 'criminal sexual assault'
WHERE primary_type = 'crim sexual assault'

SELECT 
    primary_type, 
    community_area, 
    domestic, 
    count(primary_type) AS num_crimes
FROM crime
WHERE year = 2022
GROUP BY primary_type, community_area, domestic