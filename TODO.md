You are a senior software engineer. You need to create a basic django project with 4 endpoints unauthenticated endpoints.
One is a GET endpoint that connects to a postgres database and returns data from a table called "SoilMoisture". This table will have following columns:
id (uuid)
data (JSONB)
metadata (JSONB, optional)
ip_address (varchar)
created_at (timestamp)
updated_at (timestamp)

The other 2 endpoints are for creating, updating and deleting data from the "SoilMoisture" table.


The code must have proper logging, error handling, input validation and structured response formatting.

Make sure to use the latest version of django and django rest framework.