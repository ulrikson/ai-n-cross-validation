# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

-   Run: `python main.py [mode]` (mode options: fast/f, comprehensive/c, max/m)
-   Install: `pip install -r requirements.txt`
-   Set up environment: `python -m venv venv && source venv/bin/activate`

## Code Style Guidelines

-   Use functional programming approach (avoid OOP)
-   Keep files short (under 200 lines)
-   Methods should have at most 2 parameters (dyadic) unless absolutely necessary
-   Methods should be short. They should do one thing and do it well. Preferably no more than 5 lines per method.
-   Avoid boolean parameters - they often indicate a method doing more than one thing
-   Follow KISS and YAGNI principles - don't over-engineer
-   Typing: Always use type hints (from typing import List, Dict, Any, etc.)
-   Imports: Group standard library, third-party, and local imports with a blank line between groups
-   Naming: snake_case for functions/variables, PascalCase for classes, UPPER_CASE for constants
-   Functions: Write pure functions when possible, with clear docstrings
-   Error handling: Use try/except blocks with specific exceptions
-   Structure: Store prompts in markdown files in the prompts/ directory
-   Formatting: 4-tab indentation, 120-character line length
-   Prefer using rich library for console output with appropriate colors
