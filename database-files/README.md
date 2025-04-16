# `database-files` Folder

When you start the Docker containers with docker-compose up, the MySQL container reads all the .sql files in this directory in alphabetical order and executes them to set up the database. This process happens automatically the first time the database is created.

If you need to reset the database to its initial state, you can follow these steps:

1. Stop all running containers:
    docker compose down db

2. Rebuild and restart the containers:
    docker compose up db -d

If you want to view or modify the schema, visit fitgo.sql for the DDL.
If you want to view or modify the data in our database, view fitgo_mock_data.sql for the DML.

Troubleshooting our program involves looking at our docker container logs, either manually using Docker Desktop or 
    docker compose logs db