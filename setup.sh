#!/bin/bash
# Setup Script for AI Resume ATS Checker (Linux/macOS)

echo "🎯 AI Resume ATS Checker - Setup Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Check Python
echo -e "${YELLOW}Checking Python installation...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python found: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python not found. Please install Python 3.11+${NC}"
    exit 1
fi

# Check Node.js
echo -e "${YELLOW}Checking Node.js installation...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js found: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

echo ""
echo -e "${CYAN}Setting up Backend...${NC}"
echo "--------------------"

# Backend setup
cd backend

# Create virtual environment
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists${NC}"
else
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install requirements
echo -e "${YELLOW}Installing Python dependencies...${NC}"
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install Python dependencies${NC}"
    exit 1
fi

# Download spaCy model
echo -e "${YELLOW}Downloading spaCy language model...${NC}"
python -m spacy download en_core_web_sm

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ spaCy model downloaded${NC}"
else
    echo -e "${RED}✗ Failed to download spaCy model${NC}"
    exit 1
fi

# Return to root
cd ..

echo ""
echo -e "${CYAN}Setting up Frontend...${NC}"
echo "--------------------"

# Frontend setup
cd frontend

echo -e "${YELLOW}Installing Node.js dependencies...${NC}"
npm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Node.js dependencies installed${NC}"
else
    echo -e "${RED}✗ Failed to install Node.js dependencies${NC}"
    cd ..
    exit 1
fi

# Return to root
cd ..

echo ""
echo "========================================"
echo -e "${GREEN}✓ Setup Complete!${NC}"
echo "========================================"
echo ""
echo -e "${YELLOW}To run the application:${NC}"
echo ""
echo -e "${CYAN}Terminal 1 (Backend):${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo -e "${CYAN}Terminal 2 (Frontend):${NC}"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo -e "${GREEN}Then visit: http://localhost:3000${NC}"
echo ""
