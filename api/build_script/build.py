import PyInstaller.__main__
import os
import sys
import shutil

# Ensure we're in the correct directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(script_dir))
os.chdir(script_dir)

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Define path separator based on OS
separator = ';' if os.name == 'nt' else ':'

# Define build parameters
build_args = [
    '../api.py',  # Main program entry
    '--name=DiamondAnalyzerAPI',  # Output exe name
    '--clean',  # Clean temporary files
    '--noconfirm',  # Don't ask for confirmation
    # Include icon
    f'--icon={os.path.join(project_root, "icons/icons.ico")}',  # Program icon
    # Include lib directory and its contents
    f'--add-data={os.path.join(project_root, "lib/*")}{separator}lib/',
    f'--add-data={os.path.join(project_root, "lib/__init__.py")}{separator}lib/',
    # Include configuration files
    f'--add-data=../.env{separator}.',
    f'--add-data=../api.txt{separator}.',
    # Hidden imports
    '--hidden-import=waitress',
    '--hidden-import=flask',
    '--hidden-import=lib.DiamondManager',
    '--hidden-import=lib.DiamondAnalyser',
    # Path settings
    '--paths=.',
    f'--paths={project_root}',
    # Build settings
    '--onefile',  # Generate single exe file
]

# Platform specific settings
if os.name == 'nt':  # Windows
    build_args.extend([
        '--console',  # Show console window
    ])
else:  # Linux/Mac
    build_args.extend([
        '--console',
    ])

# Run PyInstaller
try:
    PyInstaller.__main__.run(build_args)
    
    # Post-build steps
    dist_dir = os.path.join(script_dir, 'dist')
    if not os.path.exists(dist_dir):
        os.makedirs(dist_dir)
    
    # Copy configuration files to dist
    files_to_copy = {
        '.env': os.path.join(os.path.dirname(script_dir), '.env'),
        'api.txt': os.path.join(os.path.dirname(script_dir), 'api.txt')
    }
    
    for dest_name, source_path in files_to_copy.items():
        if os.path.exists(source_path):
            try:
                shutil.copy2(source_path, os.path.join(dist_dir, dest_name))
                print(f"Copied {dest_name} to dist directory")
            except Exception as e:
                print(f"Warning: Failed to copy {dest_name}: {str(e)}")
    
    print("\nBuild completed successfully!")
    print(f"Executable can be found in: {dist_dir}")
    print("\nImportant files copied to dist directory:")
    print("- .env (current configuration)")
    print("- api.txt (API documentation)")
    print("\nMake sure to review and update the .env file in the dist directory if needed.")
    
except Exception as e:
    print(f"Error occurred during build: {str(e)}")
    sys.exit(1)