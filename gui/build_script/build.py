import PyInstaller.__main__
import os
import sys

# Ensure we're in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
os.chdir(script_dir)

# Add project root to Python path
sys.path.append(project_root)

# Define build parameters
build_args = [
    '../gui.py',  # Main program entry
    '--name=DiamondAnalyzer',  # Output exe name
    '--windowed',  # Use GUI mode, no console
    '--clean',  # Clean temporary files
    '--noconfirm',  # Don't ask for confirmation
    f'--icon={os.path.join(project_root, "icons/icons.ico")}',  # Program icon
    '--add-data=../settings.json;.',  # Include settings file
    f'--add-data={os.path.join(project_root, "lib/*")};lib/',  # Include lib directory
    '--hidden-import=pandas',  # Ensure pandas is included
    '--hidden-import=numpy',
    '--hidden-import=matplotlib',
    '--hidden-import=lib.DiamondManager',  # Explicitly include lib module
    '--hidden-import=lib.DiamondAnalyser',
    '--onefile',  # Generate single exe file
    # Add paths for Linux
    '--paths=.',
    f'--paths={project_root}',
]

# Run PyInstaller
try:
    PyInstaller.__main__.run(build_args)
    print("Build completed successfully!")
except Exception as e:
    print(f"Error occurred during build: {str(e)}")
    sys.exit(1) 