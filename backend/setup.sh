#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Moi AIMER Toi - Backend Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo -e "${YELLOW}Node.js is not installed. Please install Node.js first.${NC}"
    echo "Visit: https://nodejs.org/"
    exit 1
fi

echo -e "${GREEN}✓ Node.js is installed${NC}"

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo -e "${YELLOW}npm is not installed. Please install npm first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ npm is installed${NC}"

# Install dependencies
echo -e "\n${BLUE}Installing dependencies...${NC}"
npm install

# Create uploads directory
if [ ! -d "uploads" ]; then
    mkdir uploads
    echo -e "${GREEN}✓ Created uploads directory${NC}"
fi

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\nTo start the server, run:"
echo -e "${BLUE}npm start${NC}"
echo -e "\nThe API will be available at:"
echo -e "${BLUE}http://localhost:3001${NC}"
