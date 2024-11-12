# Diamond Analyzer Project

This project consists of two main components:
1. A GUI application for analyzing diamonds
2. An API server for providing diamond analysis services

## Prerequisites

Before building the project, ensure you have:
- Python 3.8 or higher installed
- pip (Python package manager)
- Git (for cloning the repository)

## Project Structure

diamond-analyzer/
├── api/                  # API server
│   ├── api.py           # Main API file
│   ├── api.txt          # API documentation
│   ├── config.py        # API configuration
│   ├── .env             # Environment variables
│   └── build_script/    # API build scripts
├── gui/                 # GUI application
│   ├── gui.py          # Main GUI file
│   ├── config.py       # GUI configuration
│   ├── settings.json   # GUI settings
│   └── build_script/   # GUI build scripts
├── lib/                # Shared library
│   ├── DiamondManager.py
│   └── diamondAnalyser.py
└── icons/             # Application icons

## Building and Running

### GUI Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```
2. Build the application:
```bash
# Windows
cd gui/build_script
python build.py

# Linux/Mac
cd gui/build_script
python3 build.py
chmod +x dist/DiamondAnalyzer
```
3. Run the application:
- Windows: Double-click dist/DiamondAnalyzer.exe
- Linux/Mac: ./dist/DiamondAnalyzer

### API Server

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Build the server:
```bash
# Windows
cd api/build_script
python build.py

# Linux/Mac
cd api/build_script
python3 build.py
chmod +x dist/DiamondAnalyzerAPI
```
3. Configure the server:

* Edit .env file to set your configuration

4. Run the server:
- Windows: Double-click dist/DiamondAnalyzerAPI.exe
- Linux/Mac: ./dist/DiamondAnalyzerAPI


## Configuration

### GUI Configuration
- Settings are stored in gui/settings.json
- Language and server URL can be configured through the GUI

### API Configuration
Edit .env file to configure:
- FULLNODE_URL: URL of the fullnode server
- FLASK_ENV: 'development' or 'production'
- FLASK_HOST: Server host (use '0.0.0.0' for production)
- FLASK_PORT: Server port number

## Common Issues

### Linux/Mac Specific
1. GUI not starting:

sudo apt-get install python3-tk  # For Ubuntu/Debian

2. Permission issues:

chmod +x dist/DiamondAnalyzer
chmod +x dist/DiamondAnalyzerAPI

### Windows Specific
1. If antivirus blocks the executable, add an exception
2. Run as administrator if needed

### General Issues
1. Module not found errors:
   - Ensure all dependencies are installed
   - Check if you're in the correct directory
   - Verify Python path is set correctly

2. Configuration issues:
   - Verify settings.json exists for GUI
   - Check .env configuration for API
   - Ensure FULLNODE_URL is accessible



