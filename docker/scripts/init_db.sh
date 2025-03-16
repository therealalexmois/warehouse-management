#!/bin/bash

# Ensure the db folder exists
mkdir -p db

# Check if database already exists
if [ ! -f "db/warehouse.db" ]; then
    echo "Creating SQLite database..."
    touch db/warehouse.db
else
    echo "Database already exists."
fi

echo "Setting correct permissions..."
chmod 777 db
chmod 666 db/warehouse.db

echo "SQLite database is ready."
