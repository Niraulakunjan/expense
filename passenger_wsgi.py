import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense.settings')

# LiteSpeed/Passenger uses WSGI protocol — must use WSGI entry point here
# WebSocket support via Channels requires running Daphne separately on a port
from expense.wsgi import application
