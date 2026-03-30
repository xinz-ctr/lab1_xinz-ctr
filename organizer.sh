#!/bin/bash

# Create archive folder if it doesn't exist
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Generate timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# Check if grades.csv exists
if [ -f "grades.csv" ]; then

    new_name="grades_$timestamp.csv"

    # Move file to archive
    mv grades.csv archive/$new_name

    # Create new empty file
    touch grades.csv

    # Log operation
    echo "$timestamp | grades.csv -> archive/$new_name" >> organizer.log

    echo "File archived successfully."

else
    echo "grades.csv not found."
fi
