#!/bin/zsh

# Markdown Linting Script
# Removes AI markers, fixes formatting, converts to Markdeep markdown style

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 <input_markdown_file>"
    echo ""
    echo "Description:"
    echo "  Lints a markdown file by removing AI markers, fixing formatting,"
    echo "  and converting to Markdeep markdown style."
    echo ""
    echo "Arguments:"
    echo "  input_markdown_file    Path to the markdown file to lint"
    echo ""
    echo "Output:"
    echo "  Creates a new file with 'linted.md' suffix in the same directory"
    echo ""
    echo "Example:"
    echo "  $0 ./article.md              # Creates ./article-linted.md"
    echo "  $0 ~/docs/notes.md           # Creates ~/docs/notes-linted.md"
    exit 1
}

# Function to clean markdown content
lint_markdown() {
    local content="$1"
    
    # Remove common AI markers and artifacts
    content=$(echo "$content" | sed -E '
        # Remove thinking/reasoning blocks
        /<think>/,/<\/think>/d
        /\*\*Thinking\*\*/,/^$/d
        /```thinking/,/```/d
        
        # Remove assistant markers
        /^\[Assistant\]/d
        /^\[AI\]/d
        /^Assistant:/d
        /^AI:/d
        
        # Remove XML-style tags
        /</,/<\/antml:/d
        /<citation/,/<\/citation>/d
        
        # Remove excessive blank lines (more than 2 consecutive)
        /^$/N;/^\n$/N;/^\n\n$/d
        
        # Remove trailing whitespace
        s/[[:space:]]+$//
        
        # Remove leading/trailing blank lines will be handled at the end
    ')
    
    # Fix common formatting issues
    content=$(echo "$content" | awk '
        BEGIN { in_code_block = 0; prev_blank = 0 }
        
        # Track code blocks
        /^```/ {
            in_code_block = !in_code_block
            print
            prev_blank = 0
            next
        }
        
        # Preserve content inside code blocks
        in_code_block {
            print
            prev_blank = 0
            next
        }
        
        # Handle blank lines
        /^[[:space:]]*$/ {
            if (prev_blank == 0) {
                print ""
                prev_blank = 1
            }
            next
        }
        
        # Fix header spacing (ensure one blank line before headers)
        /^#{1,6} / {
            if (NR > 1 && prev_blank == 0) print ""
            print
            prev_blank = 0
            next
        }
        
        # Fix list item spacing
        /^[[:space:]]*[-*+] / || /^[[:space:]]*[0-9]+\. / {
            print
            prev_blank = 0
            next
        }
        
        # Regular lines
        {
            print
            prev_blank = 0
        }
    ')
    
    # Convert to Markdeep-style enhancements
    content=$(echo "$content" | sed -E '
        # Fix emphasis (ensure proper spacing)
        s/\*\*([^*]+)\*\*/\*\*\1\*\*/g
        s/\*([^*]+)\*/\*\1\*/g
        
        # Fix code spans (ensure no space inside backticks)
        s/` ([^`]+) `/`\1`/g
        
        # Ensure links have proper format
        s/\[([^\]]+)\]\(([^)]+)\)/[\1](\2)/g
        
        # Fix blockquote spacing
        s/^>[[:space:]]+/> /
    ')
    
    echo "$content"
}

# Check if input file is provided
if [[ $# -eq 0 ]]; then
    echo "${RED}Error: No input file specified${NC}"
    usage
fi

INPUT_FILE="$1"

# Check for help flag
if [[ "$INPUT_FILE" == "-h" || "$INPUT_FILE" == "--help" ]]; then
    usage
fi

# Validate input file
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "${RED}Error: Input file '$INPUT_FILE' does not exist${NC}"
    exit 1
fi

# Check if it's a markdown file
if [[ ! "$INPUT_FILE" =~ \.(md|markdown)$ ]]; then
    echo "${RED}Error: Input file must be a markdown file (.md or .markdown)${NC}"
    exit 1
fi

# Generate output filename
INPUT_DIR=$(dirname "$INPUT_FILE")
INPUT_BASENAME=$(basename "$INPUT_FILE" | sed -E 's/\.(md|markdown)$//')
OUTPUT_FILE="${INPUT_DIR}/${INPUT_BASENAME}-linted.md"

# Check if output file already exists
if [[ -f "$OUTPUT_FILE" ]]; then
    echo "${YELLOW}Warning: Output file '$OUTPUT_FILE' already exists${NC}"
    read "REPLY?Overwrite? (y/N): "
    if [[ ! "$REPLY" =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 0
    fi
fi

echo "${YELLOW}Starting markdown linting...${NC}"
echo "Input:  $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo ""

# Read the entire file
CONTENT=$(cat "$INPUT_FILE")

# Apply linting
LINTED_CONTENT=$(lint_markdown "$CONTENT")

# Trim leading and trailing blank lines
LINTED_CONTENT=$(echo "$LINTED_CONTENT" | sed -e :a -e '/^\n*$/{$d;N;ba' -e '}')

# Write to output file
echo "$LINTED_CONTENT" > "$OUTPUT_FILE"

# Add Markdeep script tag at the end if not present
if ! grep -q "markdeep" "$OUTPUT_FILE"; then
    cat >> "$OUTPUT_FILE" << 'EOF'

<!-- Markdeep: --><style class="fallback">body{visibility:hidden;white-space:pre;font-family:monospace}</style><script src="markdeep.min.js" charset="utf-8"></script><script src="https://casual-effects.com/markdeep/latest/markdeep.min.js" charset="utf-8"></script><script>window.alreadyProcessedMarkdeep||(document.body.style.visibility="visible")</script>
EOF
fi

echo ""
echo "${GREEN}✓ Linting complete!${NC}"
echo "Output saved to: $OUTPUT_FILE"

# Show statistics
ORIGINAL_LINES=$(wc -l < "$INPUT_FILE" | tr -d ' ')
LINTED_LINES=$(wc -l < "$OUTPUT_FILE" | tr -d ' ')
echo ""
echo "Statistics:"
echo "  Original: $ORIGINAL_LINES lines"
echo "  Linted:   $LINTED_LINES lines"
