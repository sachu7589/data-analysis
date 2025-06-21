#!/bin/bash

echo "Building Docker container for analysis project..."

# Build the Docker image
docker build -t analysis-project .

echo "Build complete! You can now run:"
echo "  docker run -p 5000:5000 analysis-project"
echo "  or"
echo "  docker-compose up" 