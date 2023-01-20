-- Import 2023 data using import wizard

-- Insert entries into main crime table
INSERT INTO crime(
    [date], district, [block], latitude, [description], 
    location_description, updated_on, community_area,
    iucr, ward, case_number, [year], domestic, fbi_code, 
    longitude, beat, primary_type, arrest, id
)
    SELECT
        [date], district, [block], latitude, [description], 
        location_description, updated_on, community_area,
        iucr, ward, case_number, [year], domestic, fbi_code, 
        longitude, beat, primary_type, arrest, id
    FROM dbo.crimes2013
GO

-- Drop table, repeat for 2022-2013
DROP TABLE dbo.crimes2013

select COUNT(id)
from crime