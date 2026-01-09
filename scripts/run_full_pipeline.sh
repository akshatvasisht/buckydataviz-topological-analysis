#!/bin/bash
#
# Full reproducibility pipeline for Big Ten Fight Song TDA Analysis
#
# This script runs the complete analysis pipeline from raw data to final
# visualizations and statistical reports. All outputs are deterministic
# (random_state=42) for reproducibility.
#
# Usage: bash scripts/run_full_pipeline.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Big Ten Fight Song TDA - Full Reproducibility Pipeline      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check dependencies
echo -e "${YELLOW}[1/7]${NC} Checking dependencies..."
if ! python3 -c "import pandas, numpy, scipy, sklearn, kmapper, matplotlib, seaborn" 2>/dev/null; then
    echo -e "${RED}[ERROR]${NC} Missing dependencies. Please run 'pip install -r requirements.txt'"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} All dependencies installed"
echo ""

# Step 2: Validate raw data
echo -e "${YELLOW}[2/7]${NC} Validating raw data..."
if [ -f "$PROJECT_DIR/data/fight-songs.csv" ]; then
    LINES=$(wc -l < "$PROJECT_DIR/data/fight-songs.csv")
    echo -e "${GREEN}[OK]${NC} Raw data found: $LINES lines"
else
    echo -e "${RED}[ERROR]${NC} Error: data/fight-songs.csv not found!"
    echo "   Download from: https://github.com/fivethirtyeight/data/tree/master/fight-songs"
    exit 1
fi
echo ""

# Step 3: Data preprocessing
echo -e "${YELLOW}[3/7]${NC} Running data preprocessing..."
cd "$PROJECT_DIR"
python src/preprocess.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK]${NC} Preprocessing complete"
else
    echo -e "${RED}[ERROR]${NC} Preprocessing failed"
    exit 1
fi
echo ""

# Step 4: Generate TDA visualization
echo -e "${YELLOW}[4/7]${NC} Generating TDA visualization..."
python src/visualize.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK]${NC} Visualization generated"
else
    echo -e "${RED}[ERROR]${NC} Visualization failed"
    exit 1
fi
echo ""

# Step 5: Enhance visualization
echo -e "${YELLOW}[5/7]${NC} Enhancing visualization with Wisconsin theme..."
python src/enhance_visualization.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK]${NC} Visualization enhanced"
else
    echo -e "${RED}[ERROR]${NC} Enhancement failed"
    exit 1
fi
echo ""

# Step 6: Generate companion plots
echo -e "${YELLOW}[6/7]${NC} Generating companion plots..."
python src/generate_companion_plots.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK]${NC} Companion plots generated"
else
    echo -e "${RED}[ERROR]${NC} Companion plot generation failed"
    exit 1
fi
echo ""

# Step 7: Statistical validation
echo -e "${YELLOW}[7/7]${NC} Running statistical validation..."
python src/statistical_validation.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK]${NC} Statistical validation complete"
else
    echo -e "${RED}[ERROR]${NC} Statistical validation failed"
    exit 1
fi
echo ""

# Summary
echo -e "${GREEN}╔════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Pipeline execution complete!                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}Generated Artifacts:${NC}"
echo "  - Interactive Visualization: docs/index.html"
echo "  - Companion Plots: docs/images/*.png"
echo "  - Statistical Report: data/correlation_analysis.csv"
echo "  - EDA Notebook: notebooks/exploratory_analysis.ipynb"
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Open visualization: ${GREEN}open docs/index.html${NC}"
echo "  2. Review findings: ${GREEN}cat docs/FINDINGS.md${NC}"
echo "  3. Run EDA notebook: ${GREEN}jupyter notebook notebooks/exploratory_analysis.ipynb${NC}"
echo "  4. Run tests: ${GREEN}pytest tests/ -v${NC}"
echo ""
echo -e "${YELLOW}On, Wisconsin!${NC}"
