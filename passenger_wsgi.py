# passenger_wsgi.py
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Import your FastAPI app
from app.main import app as application