#!/bin/zsh

# ------------------------------------------------------------------------------
# [[Mode]]: Build
# [[Context]]: The Provenance Shield (Git Scrubber)
# [[Priority]]: High
# [[ActionType]]: Scaffold
# [[TargetZone]]: scripts/
# [[SpecialNotes]]: Destructive operation; removes history and sensitive files.
# ------------------------------------------------------------------------------

# The Provenance Shield
# Purpose: Remove sensitive files from git history and enforce .gitignore.

set -e

# Colors (using ANSI-C quoting for cross-shell compatibility)
RED=$'\033[0;31m'
GREEN=$'\033[0;32m'
YELLOW=$'\033[1;33m'
BLUE=$'\033[0;34m'
NC=$'\033[0m' # No Color

echo "${BLUE}🛡️  The Provenance Shield: Git History Scrubber & Sanitizer 🛡️${NC}"
echo "${YELLOW}WARNING: This script rewrites git history. It is DESTRUCTIVE.${NC}"
echo "${YELLOW}Ensure you have a backup of your repository before proceeding.${NC}"
echo ""

# Check if inside a git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "${RED}Error: Not a git repository.${NC}"
    exit 1
fi

# Check for git-filter-repo
if ! git filter-repo --version > /dev/null 2>&1; then
    echo "${RED}Error: 'git-filter-repo' is not found.${NC}"
    echo "Please install it (e.g., 'brew install git-filter-repo' or 'pip install git-filter-repo')."
    exit 1
fi

echo "Current Repository: $(git rev-parse --show-toplevel)"
echo ""
echo "${RED}Are you sure you want to proceed? (yes/no)${NC}"
read "confirmation?-> "

if [[ "$confirmation" != "yes" ]]; then
    echo "Aborted."
    exit 0
fi

# 0. Create Backup
echo ""
echo "${BLUE}Step 0: Creating local backup...${NC}"
timestamp=$(date +%Y%m%d_%H%M%S)
backup_file="provenance_backup_${timestamp}.tar.gz"

# Create tarball, excluding existing backups to prevent recursion
# We exclude the .git directory if it's too large? User asked for backup.
# Usually backup of a git repo includes .git so you can restore state.
echo "Archiving current directory (including .git history)..."
tar --exclude='provenance_backup_*.tar.gz' -czf "$backup_file" .

echo "${GREEN}Backup saved to: $(pwd)/$backup_file${NC}"

# Ensure backup is ignored in .gitignore
if [ ! -f .gitignore ]; then
    touch .gitignore
fi

if ! grep -q "provenance_backup_" .gitignore; then
    echo "" >> .gitignore
    echo "# Provenance Shield Backups" >> .gitignore
    echo "provenance_backup_*.tar.gz" >> .gitignore
    echo "Added backup pattern to .gitignore."
fi

# 1. Define Sensitive Patterns
# Add common sensitive patterns here
typeset -a sensitive_patterns
sensitive_patterns=(
    ".env"
    ".env.local"
    ".env.production"
    "*.pem"
    "*.key"
    "*.p12"
    "id_rsa"
    "id_dsa"
    "*.kdbx"
    "secrets.json"
    "credentials.json"
)

echo ""
echo "${BLUE}Default sensitive patterns to scrub from HISTORY:${NC}"
for pattern in "${sensitive_patterns[@]}"; do
    echo "  - $pattern"
done
echo ""
echo "Do you want to add more patterns? (y/n)"
read "add_more?-> "

if [[ "$add_more" == "y" || "$add_more" == "Y" ]]; then
    echo "Enter patterns separated by space (e.g., config.yaml *.secret):"
    read "user_patterns"
    # Split string into array
    sensitive_patterns+=(${=user_patterns})
fi

# Build arguments for git-filter-repo
filter_args=()
for pattern in "${sensitive_patterns[@]}"; do
    # Check if it's a glob (contains *)
    if [[ "$pattern" == *"*"* ]]; then
        filter_args+=(--path-glob "$pattern")
    else
        filter_args+=(--path "$pattern")
    fi
done

# 2. Scrub History
echo ""
echo "${BLUE}Step 1: Scrubbing history...${NC}"
# We use --invert-paths to KEEP everything EXCEPT the matches.
# Using --force because we are running in an existing repo (destructive).
# Note: git-filter-repo usually refuses to run on a non-fresh clone unless --force is used.
git filter-repo "${filter_args[@]}" --invert-paths --force

echo "${GREEN}History scrubbed.${NC}"

# 3. Refresh .gitignore
echo ""
echo "${BLUE}Step 2: Refreshing .gitignore enforcement...${NC}"
echo "This will untrack any files that are currently ignored by .gitignore but were tracked."

# Ensure we are on a branch
current_branch=$(git branch --show-current)
if [[ -z "$current_branch" ]]; then
    echo "${YELLOW}Detached HEAD detected. Checking out main or master...${NC}"
    git checkout main 2>/dev/null || git checkout master 2>/dev/null || echo "Could not checkout main/master. Staying on detached HEAD."
fi

# Remove everything from index (not working tree)
git rm -r --cached . > /dev/null

# Re-add everything
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "No .gitignore violations found in the current index."
else
    echo "Committing .gitignore enforcement changes..."
    git commit -m "chore: refresh .gitignore enforcement (The Provenance Shield)"
fi

echo "${GREEN}.gitignore refreshed.${NC}"

# 4. Final Cleanup (Aggressive GC)
echo ""
echo "${BLUE}Step 3: Aggressive Garbage Collection...${NC}"
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo ""
echo "${GREEN}🛡️  The Provenance Shield has completed its task. 🛡️${NC}"
echo "Your repository history has been rewritten."
echo "${YELLOW}IMPORTANT: You must force-push to your remote: 'git push --force --all'${NC}"
