#!/bin/zsh

# Whisper Media Transcription Script
# Transcribes audio/video files to markdown format

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display usage
usage() {
    echo "Usage: $0 -i <input_file> -o <output_file> [-m <model>]"
    echo ""
    echo "Options:"
    echo "  -i    Input media file (audio/video)"
    echo "  -o    Output markdown file path"
    echo "  -m    Whisper model (tiny, base, small, medium, large) [default: base]"
    echo ""
    echo "Example:"
    echo "  $0 -i ./audio.mp3 -o ./transcript.md"
    echo "  $0 -i ~/video.mp4 -o ~/Documents/transcript.md -m small"
    exit 1
}

# Default values
MODEL="base"
INPUT_FILE=""
OUTPUT_FILE=""

# Parse command line arguments
while getopts "i:o:m:h" opt; do
    case $opt in
        i)
            INPUT_FILE="$OPTARG"
            ;;
        o)
            OUTPUT_FILE="$OPTARG"
            ;;
        m)
            MODEL="$OPTARG"
            ;;
        h)
            usage
            ;;
        \?)
            echo "${RED}Invalid option: -$OPTARG${NC}" >&2
            usage
            ;;
    esac
done

# Validate required arguments
if [[ -z "$INPUT_FILE" || -z "$OUTPUT_FILE" ]]; then
    echo "${RED}Error: Input and output files are required${NC}"
    usage
fi

# Check if input file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "${RED}Error: Input file '$INPUT_FILE' does not exist${NC}"
    exit 1
fi

# Check if whisper is installed
if ! command -v whisper &> /dev/null; then
    echo "${RED}Error: whisper is not installed${NC}"
    echo "Install with: pip install openai-whisper"
    exit 1
fi

# Create output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
mkdir -p "$OUTPUT_DIR"

# Get filename without extension for metadata
BASENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "${YELLOW}Starting transcription...${NC}"
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Model: $MODEL"
echo ""

# Run whisper and capture output
# Note: whisper automatically names output files based on input filename
# Parameters optimized for long-form content (1+ hour)
whisper "$INPUT_FILE" \
    --model "$MODEL" \
    --output_format txt \
    --output_dir "$OUTPUT_DIR" \
    --task transcribe \
    --condition_on_previous_text True \
    --patience 2.0 \
    --beam_size 5 \
    --best_of 5 \
    --temperature 0 \
    --compression_ratio_threshold 2.4 \
    --logprob_threshold -1.0 \
    --no_speech_threshold 0.6

# Whisper creates output based on input filename
INPUT_BASENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')
TEMP_OUTPUT="${OUTPUT_DIR}/${INPUT_BASENAME}.txt"

# Check if transcription succeeded
if [[ ! -f "$TEMP_OUTPUT" ]]; then
    echo "${RED}Error: Transcription failed${NC}"
    exit 1
fi

# Convert to markdown with metadata
cat > "$OUTPUT_FILE" << EOF
---
title: Transcript - $BASENAME
date: $TIMESTAMP
source: $INPUT_FILE
model: whisper-$MODEL
---

# Transcript: $BASENAME

**Source File:** \`$(basename "$INPUT_FILE")\`  
**Transcription Date:** $TIMESTAMP  
**Model:** whisper-$MODEL

---

## Content

$(cat "$TEMP_OUTPUT")

---

*Transcribed using OpenAI Whisper*
EOF

# Clean up temporary file
rm -f "$TEMP_OUTPUT"

echo ""
echo "${GREEN}✓ Transcription complete!${NC}"
echo "Output saved to: $OUTPUT_FILE"
