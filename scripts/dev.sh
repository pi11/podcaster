#!/bin/bash
# Development#!/bin/bash
# Development helper script

set -e

case "$1" in
    "install")
        echo "📦 Installing dependencies..."
        poetry install
        ;;
    "format")
        echo "🎨 Formatting code..."
        poetry run black app/
        poetry run isort app/
        ;;
    "lint")
        echo "🔍 Linting code..."
        poetry run mypy app/
        ;;
    "test")
        echo "🧪 Running tests..."
        poetry run pytest
        ;;
    "cli")
        shift
        echo "🎯 Running CLI command: $@"
        poetry run podcast "$@"
        ;;
    "clean")
        echo "🧹 Running cleanup..."
        poetry run podcast cleanup --dry-run
        read -p "Continue with actual cleanup? (y/N) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            poetry run podcast cleanup
        fi
        ;;
    *)
        echo "Usage: $0 {install|format|lint|test|cli|clean}"
        echo "Examples:"
        echo "  $0 install          # Install dependencies"
        echo "  $0 format           # Format code"
        echo "  $0 cli status       # Run CLI status command"
        echo "  $0 clean           # Interactive cleanup"
        exit 1
        ;;
esac


