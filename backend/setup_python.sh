#!/bin/bash

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Moi AIMER Toi - Python Backend Setup${NC}"
echo -e "${BLUE}========================================${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}Python 3 is not installed. Please install Python 3.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Python 3 is installed${NC}"
python3 --version

# Install dependencies
echo -e "\n${BLUE}Installing Python dependencies...${NC}"
pip3 install -r requirements.txt

echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\nTo start the server, run:"
echo -e "${BLUE}python3 app.py${NC}"
echo -e "\nThe API will be available at:"
echo -e "${BLUE}http://localhost:3001${NC}"
