import os
import sys
import pymysql

pymysql.version_info = (2, 2, 1, 'final', 0)
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_project.settings')

# LiteSpeed/Passenger uses WSGI protocol — must use WSGI entry point here
# WebSocket support via Channels requires running Daphne separately on a port
from expense_project.wsgi import application
