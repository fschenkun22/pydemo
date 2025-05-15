import sys

# Display the full version string
print(f"Python version: {sys.version}")

# Display version components
version_info = sys.version_info
print(f"Python version: {version_info.major}.{version_info.minor}.{version_info.micro}")