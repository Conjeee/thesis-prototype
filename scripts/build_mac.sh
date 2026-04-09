#!/bin/bash
echo "🚀 Starting macOS Build Process..."

# 1. Sync dependencies using uv (excluding torch)
uv sync

# 2. Install PyInstaller into the virtual environment
uv pip install pyinstaller

# 3. Clean up old builds
rm -rf build/ dist/

# 4. Run PyInstaller with the macOS spec file
uv run pyinstaller scripts/mac.spec --clean

echo "✅ Build Complete! Your application is located in the dist/ folder."