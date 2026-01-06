"""
PAZ Application Entry Point.

This module allows running PAZ as a module: python -m paz
"""

import sys


def main() -> int:
    """Main entry point for PAZ application."""
    from paz.app import run_app

    return run_app()


if __name__ == "__main__":
    sys.exit(main())
