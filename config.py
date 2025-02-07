import os

# Telegram Bot Configuration
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Token will be set via environment variable

# PDF Configuration
PAGE_WIDTH = 595.27
PAGE_HEIGHT = 841.89
MARGIN = 50

# Colors
COLORS = {
    'primary': '#2c3e50',
    'secondary': '#34495e',
    'success': '#27ae60',
    'danger': '#c0392b',
    'white': '#ffffff',
}

# Font configurations
FONT_FAMILY = 'Helvetica'
FONT_SIZE_TITLE = 16
FONT_SIZE_SUBTITLE = 14
FONT_SIZE_BODY = 12

# Template configurations
TEMPLATES_DIR = 'templates'
DEFAULT_TEMPLATE = 'default'