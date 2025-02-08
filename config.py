"""Configuration settings for the hospital report bot."""

import os

# Telegram Bot Settings
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# PDF Document Settings
PAGE_WIDTH = 595.27  # A4 width in points
PAGE_HEIGHT = 841.89  # A4 height in points
MARGIN = 50

# Color Scheme
COLORS = {
    'primary': '#2c3e50',    # Dark blue
    'secondary': '#34495e',  # Lighter blue
    'success': '#27ae60',    # Green
    'danger': '#c0392b',     # Red
    'white': '#ffffff',      # White
}

# Typography
FONT_FAMILY = 'Helvetica'
FONT_SIZES = {
    'title': 16,
    'subtitle': 14,
    'body': 12,
}

# Font size constants for templates
FONT_SIZE_TITLE = FONT_SIZES['title']
FONT_SIZE_SUBTITLE = FONT_SIZES['subtitle']
FONT_SIZE_BODY = FONT_SIZES['body']

# Template Settings
TEMPLATES = {
    'directory': 'templates',
    'default': 'default',
}