#!/usr/bin/env python3
"""Branding and UI enhancements for the TDA dashboard."""

import os
import re

# --- Constants ---

# UW-Madison Color Palette
WISCONSIN_RED = '#c5050c'
WISCONSIN_DARK_RED = '#9b0000'
WISCONSIN_WHITE = '#ffffff'
WISCONSIN_LIGHT_GRAY = '#f5f5f5'
WISCONSIN_DARK_GRAY = '#646569'

# File Paths (Relative to repository root)
HTML_PATH = 'docs/index.html'

# --- CSS Template ---

WISCONSIN_THEME_CSS = f"""
<style>
    /* Wisconsin Badgers Theme */
    :root {{
        --wisconsin-red: {WISCONSIN_RED};
        --wisconsin-dark-red: {WISCONSIN_DARK_RED};
        --wisconsin-white: {WISCONSIN_WHITE};
        --wisconsin-light-gray: {WISCONSIN_LIGHT_GRAY};
        --wisconsin-dark-gray: {WISCONSIN_DARK_GRAY};
    }}

    body {{
        font-family: 'Helvetica Neue', Arial, sans-serif;
        background: linear-gradient(135deg, var(--wisconsin-light-gray) 0%, var(--wisconsin-white) 100%);
        margin: 0;
        padding: 0;
    }}

    h1, h2, h3 {{
        color: var(--wisconsin-red);
        font-weight: 700;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }}

    .info-box {{
        background-color: var(--wisconsin-white);
        border-left: 6px solid var(--wisconsin-red);
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-radius: 4px;
    }}

    .metadata {{
        background-color: var(--wisconsin-red);
        color: var(--wisconsin-white);
        padding: 15px 25px;
        border-radius: 8px;
        margin: 20px 0;
    }}

    #graph-container {{
        background-color: var(--wisconsin-white);
        border: 3px solid var(--wisconsin-red);
        border-radius: 10px;
        padding: 30px;
        margin: 30px auto;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        max-width: 1400px;
    }}

    .tooltip {{
        position: absolute;
        background-color: var(--wisconsin-white);
        border: 3px solid var(--wisconsin-red);
        border-radius: 8px;
        padding: 15px;
        font-size: 14px;
        pointer-events: none;
        box-shadow: 0 6px 16px rgba(0,0,0,0.25);
        z-index: 1000;
    }}

    .footer {{
        text-align: center;
        padding: 40px;
        background-color: var(--wisconsin-red);
        color: var(--wisconsin-white);
        margin-top: 50px;
    }}
</style>
"""

# --- HTML Templates ---

ENHANCED_HEADER = """
<div style="max-width: 1400px; margin: 0 auto; padding: 40px 20px;">
    <h1 style="text-align: center;">Big Ten Fight Song Topological Analysis</h1>
    <div class="info-box">
        <h3>Overview</h3>
        <p>This visualization applies <strong>Topological Data Analysis (TDA)</strong> to identify
        structural relationships in fight songs. Node colors represent win percentages.</p>
    </div>
    <div class="metadata">
        <h4>Methodology</h4>
        <p><strong>Clustering:</strong> DBSCAN via KeplerMapper | <strong>Projection:</strong> t-SNE</p>
    </div>
</div>
"""

ENHANCED_FOOTER = """
<div class="footer">
    <p><strong>Big Ten Fight Song TDA</strong> | Bucky's Data Viz Challenge</p>
    <p>University of Wisconsin-Madison | 2024-2025</p>
</div>
"""


def enhance_html_file(path: str) -> None:
    """Inject branding and content into KeplerMapper output."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing visualization file: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # CSS
    content = content.replace('</head>', f'{WISCONSIN_THEME_CSS}\n</head>')

    # Header/Footer
    content = content.replace('<body>', f'<body>\n{ENHANCED_HEADER}')
    content = content.replace('</body>', f'{ENHANCED_FOOTER}\n</body>')

    # Tooltip Formatting (matches KeplerMapper defaults)
    content = re.sub(
        r'<b>(.*?)</b><br><i>(.*?)</i><br><hr>Win Rate: (.*?)<br>Aggression: (.*?)/10',
        r'<h4>\1</h4><div class="song-name">\2</div><hr>'
        r'<div class="stat"><b>Win Rate:</b> \3</div>'
        r'<div class="stat"><b>Aggression:</b> \4/10</div>',
        content
    )

    # Wrap graph in styled container
    content = re.sub(
        r'<div id="graph">',
        r'<div id="graph-container"><div id="graph">',
        content
    )
    # Close container
    content = re.sub(
        r'</div>\s*</body>',
        r'</div></div></body>',
        content
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def main() -> None:
    """Run enhancement pass."""
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_target = os.path.join(root_dir, HTML_PATH)

    print(f"Applying professional branding to {HTML_PATH}...")
    enhance_html_file(html_target)
    print("Branding enhancement complete.")


if __name__ == '__main__':
    main()
