#!/bin/bash
# ============================================
#  ARTEMIS CITY - SECRET SETUP SCRIPT
# ============================================
# This script helps set up secure environment files
# Usage: ./setup_secrets.sh

set -e

echo "  Artemis City - Secure Environment Setup"
echo "============================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to generate secure random key
generate_key() {
    if command -v openssl &> /dev/null; then
        openssl rand -hex 32
    else
        python3 -c "import secrets; print(secrets.token_hex(32))"
    fi
}

# Function to check if file exists
check_file() {
    if [ -f "$1" ]; then
        echo -e "${YELLOW}  $1 already exists${NC}"
        read -p "Overwrite? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            return 1
        fi
    fi
    return 0
}

# Step 1: Root .env file
echo -e "${BLUE} Setting up root .env file...${NC}"
if check_file ".env"; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        
        # Generate and insert MCP API key
        MCP_KEY=$(generate_key)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            sed -i '' "s/your_secure_api_key_here/$MCP_KEY/" .env
        else
            sed -i "s/your_secure_api_key_here/$MCP_KEY/" .env
        fi
        
        echo -e "${GREEN} Created .env with generated MCP_API_KEY${NC}"
        
        # Set secure permissions
        chmod 600 .env
        echo -e "${GREEN} Set permissions to 600${NC}"
    else
        echo -e "${RED} .env.example not found${NC}"
        exit 1
    fi
fi

echo ""

# Step 2: Memory Layer .env file
echo -e "${BLUE} Setting up Memory Layer .env file...${NC}"
MEMORY_DIR="Artemis Agentic Memory Layer "
if [ -d "$MEMORY_DIR" ]; then
    if check_file "$MEMORY_DIR/.env"; then
        if [ -f "$MEMORY_DIR/.env.example" ]; then
            cp "$MEMORY_DIR/.env.example" "$MEMORY_DIR/.env"
            
            # Use the same MCP API key
            if [[ "$OSTYPE" == "darwin"* ]]; then
                sed -i '' "s/your_secure_api_key_here/$MCP_KEY/" "$MEMORY_DIR/.env"
            else
                sed -i "s/your_secure_api_key_here/$MCP_KEY/" "$MEMORY_DIR/.env"
            fi
            
            echo -e "${GREEN} Created Memory Layer .env with same MCP_API_KEY${NC}"
            
            # Set secure permissions
            chmod 600 "$MEMORY_DIR/.env"
            echo -e "${GREEN} Set permissions to 600${NC}"
        else
            echo -e "${RED} $MEMORY_DIR/.env.example not found${NC}"
        fi
    fi
else
    echo -e "${YELLOW}  Memory Layer directory not found${NC}"
fi

echo ""

# Step 3: Display next steps
echo -e "${GREEN} Setup complete!${NC}"
echo ""
echo " Next steps:"
echo ""
echo "1. Edit .env files and add your Obsidian API key:"
echo -e "   ${YELLOW}OBSIDIAN_API_KEY=your_obsidian_api_key_here${NC}"
echo ""
echo "2. Get your Obsidian API key:"
echo "   - Open Obsidian"
echo "   - Go to Settings → Local REST API"
echo "   - Copy the API key"
echo ""
echo "3. Start the MCP server:"
echo -e "   ${BLUE}cd \"Artemis Agentic Memory Layer \"${NC}"
echo -e "   ${BLUE}npm install${NC}"
echo -e "   ${BLUE}npm run dev${NC}"
echo ""
echo "4. In another terminal, run Python demos:"
echo -e "   ${BLUE}source .venv/bin/activate${NC}"
echo -e "   ${BLUE}python demo_city_postal.py${NC}"
echo ""
echo " Your generated MCP_API_KEY has been set in both .env files"
echo "   (both files must use the SAME key for authentication)"
echo ""
echo " For more information, see SECURITY.md"
echo ""

# Optional: Verify .gitignore is working
echo -e "${BLUE} Verifying .gitignore protection...${NC}"
if git check-ignore .env &> /dev/null; then
    echo -e "${GREEN} .env is properly ignored by git${NC}"
else
    echo -e "${RED}  WARNING: .env may not be ignored by git!${NC}"
fi

if [ -f "$MEMORY_DIR/.env" ]; then
    if git check-ignore "$MEMORY_DIR/.env" &> /dev/null; then
        echo -e "${GREEN} Memory Layer .env is properly ignored by git${NC}"
    else
        echo -e "${RED}  WARNING: Memory Layer .env may not be ignored by git!${NC}"
    fi
fi

echo ""
echo " Artemis City is ready for secure development!"
