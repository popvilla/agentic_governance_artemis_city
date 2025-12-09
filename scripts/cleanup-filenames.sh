#!/bin/bash
# ============================================
# ARTEMIS CITY - FILENAME CLEANUP SCRIPT
# ============================================
# Fixes malformed filenames:
#   - *.md.md → *.md (double extension)
#   - *.csv.md → *.csv (wrong extension)
#   - * (2).* → removes duplicates (prompts first)
#
# Usage: ./scripts/cleanup-filenames.sh [--dry-run]

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY_RUN=false

if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
    echo "🔍 DRY RUN MODE - No files will be modified"
    echo ""
fi

echo "📁 Scanning: $PROJECT_ROOT"
echo ""

# ============================================
# FIX DOUBLE EXTENSIONS: *.md.md → *.md
# ============================================
echo "═══════════════════════════════════════════"
echo "🔧 Fixing double .md.md extensions..."
echo "═══════════════════════════════════════════"

find "$PROJECT_ROOT" -type f -name "*.md.md" | while read -r file; do
    newname="${file%.md.md}.md"
    echo "  $file"
    echo "  → $newname"
    if [[ "$DRY_RUN" == false ]]; then
        mv "$file" "$newname"
    fi
done

echo ""

# ============================================
# FIX WRONG EXTENSIONS: *.csv.md → *.csv
# ============================================
echo "═══════════════════════════════════════════"
echo "🔧 Fixing .csv.md → .csv extensions..."
echo "═══════════════════════════════════════════"

find "$PROJECT_ROOT" -type f -name "*.csv.md" | while read -r file; do
    newname="${file%.csv.md}.csv"
    echo "  $file"
    echo "  → $newname"
    if [[ "$DRY_RUN" == false ]]; then
        mv "$file" "$newname"
    fi
done

echo ""

# ============================================
# LIST DUPLICATES: * (2).* files
# ============================================
echo "═══════════════════════════════════════════"
echo "⚠️  Potential duplicates found (manual review):"
echo "═══════════════════════════════════════════"

find "$PROJECT_ROOT" -type f \( -name "* (2)*" -o -name "* (1)*" \) | while read -r file; do
    echo "  $file"
done

echo ""
echo "═══════════════════════════════════════════"
if [[ "$DRY_RUN" == true ]]; then
    echo "✅ Dry run complete. Run without --dry-run to apply changes."
else
    echo "✅ Cleanup complete!"
fi
