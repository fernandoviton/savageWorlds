#!/usr/bin/env python3
"""
Savage Worlds Character Manager

A Python application for creating and managing Savage Worlds RPG characters.
Supports character creation, skill/attribute management, dice rolling, and
character sheet display.
"""

import sys
import click
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from savage_worlds_manager.ui.cli import main_cli


if __name__ == "__main__":
    main_cli()