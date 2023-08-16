import toml
import os

# Get the path to the directory containing this file. 
# This ensures the path is correct regardless of where the code is run from.
here = os.path.abspath(os.path.dirname(__file__))

# Load the pyproject.toml file and extract the version number.
project_info = toml.load(os.path.join(here, '..', 'pyproject.toml'))
__version__ = project_info['project']['version']
